# Document Q&A API

A modular FastAPI application for ingesting documents, generating embeddings, and answering natural language questions using a local LLM. Supports both local storage and S3-based persistence.

## Features

- **File Ingestion**: Upload `.txt`, `.pdf`, `.csv` files locally or via S3.
- **Embeddings**: Generate embeddings using sentence-transformers (`all-mpnet-base-v2`).
- **Vector Database**: Store embeddings in FAISS with metadata for provenance.
- **Querying**: Ask natural language questions and get answers grounded in document content.
- **S3 Integration**: Optional storage for documents and FAISS index; controlled via AUTO_S3_SAVE.
- **Reset & List**: Clear S3 buckets and list documents.

## Potential Improvements
1. List of parsed document
2. Frontend integration for simpler querying

## Installation
```bash
git clone <repo-url>
cd document-rag-plug-and-play
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Running
```bash
uvicorn app.main:app --reload
```

## API Endpoints
| Method | Path                | Description                                                         |
| ------ | ------------------- | ------------------------------------------------------------------- |
| POST   | `/ingest`           | Upload one or more documents; updates embeddings.                   |
| POST   | `/query`            | Submit a question; returns answer based on embeddings.              |
| DELETE | `/reset`            | Clear all documents and FAISS index from S3 (or local if disabled). |
| GET    | `/docs/s3`          | List all documents in the S3 bucket.                                |
| GET    | `/vector-db-status` | Shows where vector DB was loaded from (`local` or `S3`).            |


## Usage Notes
- **Chunking**: Text is split into ~500-token segments before embeddings. Adjust CHUNK_SIZE in settings for better context coverage.
- **Top K Retrieval**: top_k determines how many nearest chunks are retrieved for each query. Higher values reduce missed info but may increase hallucination risk.
- **Hallucination Control**: Prompts are engineered to answer only based on provided context; unknown info returns: "I don't know based on the provided documents."