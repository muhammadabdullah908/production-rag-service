from app.ingestion.embeddings import embed_query
from app.retrieval.vector_store import query_chunks

def retrieve_context(question: str, top_k: int = 5) -> list[dict]:
    """Embed the question and search the vector DB."""
    query_vec = embed_query(question)
    results = query_chunks(query_embedding=query_vec, top_k=top_k)
    return results