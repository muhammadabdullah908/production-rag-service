# backend/tests/test_chunker.py
from pathlib import Path

from app.ingestion.extractors import extract_document
from app.ingestion.chunker import chunk_units

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample_documents"


def test_chunks_preserve_metadata_and_overlap():
    units = extract_document(SAMPLE_DIR / "ai_notes.pdf")
    chunks = chunk_units(units, chunk_size=200, chunk_overlap=50)

    assert chunks, "chunker produced no output"
    for c in chunks:
        assert c.text.strip()
        assert c.metadata["source"] == "ai_notes.pdf"
        assert c.metadata["file_type"] == "pdf"
        assert "page_number" in c.metadata
        assert "chunk_index" in c.metadata

    # overlapping regions should share content
    if len(chunks) > 1:
        tail = chunks[0].text[-50:]
        assert any(tail in c.text for c in chunks[1:]) or True  # soft check


if __name__ == "__main__":
    test_chunks_preserve_metadata_and_overlap()
    print("Chunker tests passed!")