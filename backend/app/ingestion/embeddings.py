"""Local embedding client using Chroma's built-in ONNX engine (no PyTorch needed)."""
from __future__ import annotations

import logging
from functools import lru_cache
from chromadb.utils import embedding_functions

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def _get_embedder():
    """Load the ONNX embedding function once and cache it."""
    logger.info("Loading local ONNX embedding model: all-MiniLM-L6-v2")
    # This automatically downloads a small ~80MB ONNX model the first time it runs
    return embedding_functions.ONNXMiniLM_L6_V2()

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts. Returns list of float vectors."""
    if not texts:
        return []
    embedder = _get_embedder()
    # ONNX embedder returns a list of numpy arrays, we convert to standard lists
    vectors = embedder(texts)
    return [v.tolist() for v in vectors]

def embed_query(text: str) -> list[float]:
    """Embed a single query string."""
    return embed_texts([text])[0]