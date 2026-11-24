"""Glue service: file → hash → dedupe → extract → chunk → embed → store."""
from __future__ import annotations

import hashlib
import logging
import uuid
from pathlib import Path

from app.core.config import settings
from app.ingestion.chunker import chunk_units
from app.ingestion.embeddings import embed_texts
from app.ingestion.extractors import extract_document
from app.retrieval.vector_store import delete_document, get_collection, upsert_chunks

logger = logging.getLogger(__name__)


class DuplicateDocumentError(Exception):
    """Raised when the same file hash is already stored."""


class UnsupportedFileError(Exception):
    """Raised for file types we do not support."""


class EmptyDocumentError(Exception):
    """Raised when extraction yields no text (scanned/empty PDF)."""


def _file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _find_existing_by_hash(file_hash: str) -> str | None:
    """Check Chroma metadata for an existing doc with this hash."""
    collection = get_collection()
    existing = collection.get(where={"file_hash": file_hash}, limit=1)
    if existing["ids"]:
        return existing["metadatas"][0].get("doc_id")
    return None


def ingest_file(path: Path) -> dict:
    """Full ingestion pipeline for one file. Returns a summary dict."""
    suffix = path.suffix.lower().lstrip(".")
    if suffix not in settings.allowed_extensions:
        raise UnsupportedFileError(f"Unsupported file type: .{suffix}")

    file_hash = _file_hash(path)
    existing_id = _find_existing_by_hash(file_hash)
    if existing_id:
        raise DuplicateDocumentError(
            f"Document already exists with id={existing_id}"
        )

    units = extract_document(path)
    if not units:
        raise EmptyDocumentError("No extractable text found in document")

    chunks = chunk_units(
        units,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    if not chunks:
        raise EmptyDocumentError("Chunking produced no output")

    doc_id = str(uuid.uuid4())
    ids = [f"{doc_id}:{i}" for i in range(len(chunks))]
    texts = [c.text for c in chunks]
    metadatas = []
    for c in chunks:
        metadatas.append(
            {
                **c.metadata,
                "doc_id": doc_id,
                "file_hash": file_hash,
                "file_name": path.name,
            }
        )

    vectors = embed_texts(texts)
    upsert_chunks(ids=ids, texts=texts, embeddings=vectors, metadatas=metadatas)

    logger.info(
        "Ingested %s → doc_id=%s, %d chunks", path.name, doc_id, len(chunks)
    )
    return {
        "doc_id": doc_id,
        "file_name": path.name,
        "chunk_count": len(chunks),
    }


def list_documents() -> list[dict]:
    """Return one summary row per distinct document in the store."""
    collection = get_collection()
    all_items = collection.get(include=["metadatas"])
    seen: dict[str, dict] = {}
    for meta in all_items["metadatas"]:
        doc_id = meta.get("doc_id")
        if doc_id and doc_id not in seen:
            seen[doc_id] = {
                "doc_id": doc_id,
                "file_name": meta.get("file_name"),
                "file_type": meta.get("file_type"),
            }
    return list(seen.values())