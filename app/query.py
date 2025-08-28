from ollama import generate
from .config import settings

def answer_question(question: str, top_k=10) -> str:
    from .embeddings import vector_db, get_embedding
    q_emb = get_embedding(question)
    results = vector_db.query(q_emb, top_k=top_k)
    context = "\n".join([r["text"] for r in results])
    
    prompt = f"""
You are a helpful Q&A assistant. Use the context below to answer the question. 
You may summarize, rephrase, or combine information from the context. 
Do not make up facts not in the documents, but you can give cautious inferences if reasonable.

Context:
{context}

Question: {question}
Answer:
    """
    
    response = generate(model=settings.MODEL_NAME, prompt=prompt)
    answer = str(response.response)
    return answer
