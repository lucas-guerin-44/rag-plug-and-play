import os
from typing import List

from fastapi import UploadFile

from .s3 import download_faiss_from_s3, upload_faiss_to_s3, upload_file_to_docs_s3
from .config import settings

def save_file_to_local(file, folder="uploads"):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """Split text into chunks of roughly chunk_size tokens."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def maybe_upload_faiss():
    if settings.AUTO_S3_SAVE:
        upload_faiss_to_s3()

def maybe_download_faiss():
    if settings.AUTO_S3_SAVE:
        download_faiss_from_s3()

def maybe_upload_file(file: UploadFile):
    if settings.AUTO_S3_SAVE:
        upload_file_to_docs_s3(file)