# backend/app/ingestion/chunker.py
from dataclasses import dataclass, field
from typing import Iterable

from app.ingestion.extractors import ExtractedUnit  # adjust path if yours differs


@dataclass
class Chunk:
    text: str
    metadata: dict = field(default_factory=dict)


_SEPARATORS = ("\n\n", "\n", ". ", " ")


def chunk_units(
    units: Iterable[ExtractedUnit],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[Chunk]:
    """
    Split extracted units into overlapping chunks.

    - Tries to break on paragraph -> line -> sentence -> word boundaries.
    - Preserves original metadata (source, file_type, page/slide) on every chunk.
    - Adds a per-source `chunk_index` so citations can say "ai_notes.pdf, chunk 2".
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: list[Chunk] = []
    per_source_counter: dict[str, int] = {}

    for unit in units:
        text = unit.text.strip()
        if not text:
            continue

        source = unit.metadata.get("source", "unknown")
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Try to snap the end to a natural boundary.
            if end < len(text):
                for sep in _SEPARATORS:
                    idx = text.rfind(sep, start, end)
                    if idx > start + chunk_overlap:
                        end = idx + len(sep)
                        break

            piece = text[start:end].strip()
            if piece:
                idx = per_source_counter.get(source, 0)
                chunks.append(
                    Chunk(
                        text=piece,
                        metadata={
                            **unit.metadata,
                            "chunk_index": idx,
                            "char_start": start,
                            "char_end": end,
                        },
                    )
                )
                per_source_counter[source] = idx + 1

            if end >= len(text):
                break
            start = end - chunk_overlap

    return chunks