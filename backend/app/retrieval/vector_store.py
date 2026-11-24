"""Chroma wrapper — embedded, file-backed, no server required."""
from __future__ import annotations

import logging
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: chromadb.ClientAPI | None = None


def get_collection(name: str = "documents") -> chromadb.Collection:
    """Return (and create if needed) the persistent Chroma collection."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=settings.chroma_path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def upsert_chunks(
    ids: list[str],
    texts: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict[str, Any]],
) -> None:
    """Insert or update chunks in the vector store."""
    collection = get_collection()
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    logger.info("Upserted %d chunks", len(ids))


def query_chunks(
    query_embedding: list[float],
    top_k: int | None = None,
    where: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Similarity search. Returns list of {id, text, metadata, score}."""
    collection = get_collection()
    n = top_k or settings.top_k
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=n,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    hits: list[dict[str, Any]] = []
    if not result["ids"] or not result["ids"][0]:
        return hits

    for i, chunk_id in enumerate(result["ids"][0]):
        # Chroma cosine distance: 0 = identical, 2 = opposite.
        # Convert to similarity score in [0, 1] for the UI.
        distance = result["distances"][0][i]
        similarity = max(0.0, 1.0 - (distance / 2.0))
        hits.append(
            {
                "id": chunk_id,
                "text": result["documents"][0][i],
                "metadata": result["metadatas"][0][i],
                "score": round(similarity, 4),
            }
        )
    return hits


def delete_document(doc_id: str) -> None:
    """Remove every chunk belonging to a document (cascade delete)."""
    collection = get_collection()
    collection.delete(where={"doc_id": doc_id})
    logger.info("Deleted all chunks for doc_id=%s", doc_id)