from ollama import generate
from .config import settings

def answer_question(question: str, top_k=10, context_override: str = None) -> str:
    from .embeddings import vector_db, get_embedding

    if context_override:
        context = context_override
    else:
        q_emb = get_embedding(question)
        results = vector_db.query(q_emb, top_k=top_k)
        context = "\n".join([r["text"] for r in results])
    
    prompt = f"""
ONLY use the provided context to answer.
If the answer is not in the context, say: "I don't know based on the provided documents."

Context:
{context}

Question: {question}
Answer:
    """

    response = generate(model=settings.MODEL_NAME, prompt=prompt)
    return str(response.response)