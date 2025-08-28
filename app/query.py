from ollama import generate
from .config import settings

def answer_question(question: str, top_k=10) -> str:
    from .embeddings import vector_db, get_embedding
    q_emb = get_embedding(question)
    results = vector_db.query(q_emb, top_k=top_k)
    context = "\n".join([r["text"] for r in results])
    
    prompt = f"""
You are a precise Q&A system.
Use ONLY the text in the context below to answer.
DO NOT add any explanations, commentary, or references like "according to the context".
If the answer is not present in the context, respond exactly: "I don't know based on the provided documents."

Context:
{context}

Question: {question}
Answer:
    """
    
    response = generate(model=settings.MODEL_NAME, prompt=prompt)
    answer = str(response.response)
    return answer
