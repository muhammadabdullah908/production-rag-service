
from pathlib import Path

from app.ingestion.extractors import extract_document


def test_txt_extraction():
    file_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "sample_documents"
        / "ai_notes.txt"
    )

    result = extract_document(file_path)

    assert len(result) == 1
    assert "Artificial Intelligence" in result[0].text
    assert result[0].metadata["file_type"] == "txt"
    assert result[0].metadata["source"] == "ai_notes.txt"

    print("\nExtracted text:")
    print(result[0].text)

    print("\nMetadata:")
    print(result[0].metadata)


if __name__ == "__main__":
    test_txt_extraction()
    print("\nTXT extraction test passed!")
