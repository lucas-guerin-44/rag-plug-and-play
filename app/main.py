import os
import tempfile
from typing import List
from fastapi import FastAPI, UploadFile, File
from contextlib import asynccontextmanager

from app.s3 import clear_all_from_s3, download_faiss_from_s3, list_docs_in_s3, upload_faiss_to_s3, upload_file_to_docs_s3
from .types import QuestionRequest

from .embeddings import embed_chunks, vector_db
from .parsing import parse_file
from .utils import chunk_text, maybe_download_faiss, maybe_upload_faiss, maybe_upload_file
from .query import answer_question
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.vector_db_source = "none"
    try:
        if settings.AUTO_S3_SAVE:
            download_faiss_from_s3()
            vector_db.load()
            app.state.vector_db_source = "S3"
        else:
            vector_db.load()
            app.state.vector_db_source = "local"
        print(f"Vector DB loaded from {app.state.vector_db_source}.")
    except Exception:
        print("No existing vector DB found. Starting fresh.")
        app.state.vector_db_source = "none"
    yield
    vector_db.save()
    if settings.AUTO_S3_SAVE:
        upload_faiss_to_s3()
    print(f"Vector DB saved (source: {app.state.vector_db_source}).")

app = FastAPI(title="Document Q&A", lifespan=lifespan)

@app.post("/ingest")
async def ingest_file(files: List[UploadFile] = File(...)):
    maybe_download_faiss()
    ingested_files = []

    for file in files:
        maybe_upload_file(file)

        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file.file.seek(0)
            tmp.write(file.file.read())
            tmp.flush()
            tmp_path = tmp.name

        text = parse_file(tmp_path)
        os.remove(tmp_path)
        
        chunks = chunk_text(text)
        embed_chunks(chunks, file.filename)
        ingested_files.append(file.filename)

    vector_db.save()
    maybe_upload_faiss()

    return {"message": f"Ingested files: {', '.join(ingested_files)}"}

@app.post("/query")
def query_doc(request: QuestionRequest):
    maybe_download_faiss()
    vector_db.load()
    answer = answer_question(request.question)
    return answer

@app.delete("/reset")
def reset_all():
    if not settings.AUTO_S3_SAVE:
        return { "message": "Current config not using S3." }
    
    clear_all_from_s3()
    return {"message": "All docs and FAISS index cleared from S3."}

@app.get("/docs/s3")
def list_docs_endpoint():
    if not settings.AUTO_S3_SAVE:
        return { "message": "Current config not using S3." }
    
    docs = list_docs_in_s3()
    return {"documents": docs}

@app.get("/vector-db-status")
def vector_db_status():
    return {"vector_db_loaded_from": app.state.vector_db_source}