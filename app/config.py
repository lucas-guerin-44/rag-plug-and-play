import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    AUTO_S3_SAVE:       bool = os.getenv("AUTO_S3_SAVE", "true").lower() == "true"
    S3_ENDPOINT:        str = os.getenv("S3_ENDPOINT", 'DEFAULT_EMPTY')
    S3_ACCESS_KEY:      str = os.getenv("S3_ACCESS_KEY", 'DEFAULT_EMPTY')
    S3_SECRET_KEY:      str = os.getenv("S3_SECRET_KEY", 'DEFAULT_EMPTY')
    S3_DOCS_BUCKET:     str = os.getenv("S3_DOCS_BUCKET", 'documents')
    S3_FAISS_BUCKET:    str = os.getenv("S3_FAISS_BUCKET", 'faiss')
    VECTOR_DB_PATH:     str = os.getenv("VECTOR_DB_PATH", "faiss_index")
    MODEL_NAME:         str = os.getenv("MODEL_NAME", "OLLAMA_MODEL")
    CHUNK_SIZE:         int = os.getenv("CHUNK_SIZE", 500)

settings = Settings()
