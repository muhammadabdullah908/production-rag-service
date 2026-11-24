
from pathlib import Path

from app.ingestion.extractors import extract_document


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample_documents"


def test_all_formats():

    formats = [
        "pdf",
        "docx",
        "pptx",
        "txt",
    ]

    for extension in formats:

        file_path = SAMPLE_DIR / f"ai_notes.{extension}"

        result = extract_document(file_path)

        assert len(result) > 0
        assert all(unit.text.strip() for unit in result)

        print(f"\n{extension.upper()} extraction: PASSED")

        for unit in result:
            print("Text:", unit.text[:150])
            print("Metadata:", unit.metadata)


if __name__ == "__main__":
    test_all_formats()
    print("\nAll document extraction tests passed!")
