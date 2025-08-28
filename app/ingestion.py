import os
from fastapi import UploadFile
from .parsing import parse_file
from .embeddings import embed_chunks
from .utils import chunk_text
from .config import settings

SUPPORTED_EXTENSIONS = (".txt", ".pdf", ".csv")

def ingest_local(folder_path: str):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        text = parse_file(file_path)
        chunks = chunk_text(text, settings.CHUNK_SIZE)
        embed_chunks(chunks, file_name)
    return f"Ingested files from {folder_path}"
