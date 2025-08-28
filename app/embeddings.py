import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from .config import settings

embedding_model = SentenceTransformer("all-mpnet-base-v2")

class VectorDB:
    def __init__(self, dim=768):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embeddings: List[List[float]], metadatas: List[Dict]):
        arr = np.array(embeddings).astype("float32")
        self.index.add(arr)
        self.metadata.extend(metadatas)

    def save(self, path=settings.VECTOR_DB_PATH):
        faiss.write_index(self.index, path)
        # Save metadata
        import pickle
        with open(path + "_meta.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self, path=settings.VECTOR_DB_PATH):
        self.index = faiss.read_index(path)
        import pickle
        with open(path + "_meta.pkl", "rb") as f:
            self.metadata = pickle.load(f)

    def query(self, embedding: List[float], top_k=5):
        arr = np.array([embedding]).astype("float32")
        distances, idxs = self.index.search(arr, top_k)
        results = [self.metadata[i] for i in idxs[0]]
        return results

vector_db = VectorDB()

def get_embedding(text: str) -> List[float]:
    """Generate local embedding for a text chunk."""
    emb = embedding_model.encode(text)
    return emb.tolist()

def embed_chunks(chunks: List[str], file_name: str):
    """Generate embeddings for all chunks and add to vector DB."""
    embeddings = []
    metadatas = []
    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        embeddings.append(emb)
        metadatas.append({
            "file": file_name,
            "position": i,
            "text": chunk
        })
    vector_db.add(embeddings, metadatas)
