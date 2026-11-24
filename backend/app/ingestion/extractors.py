
from pathlib import Path

import pymupdf
from docx import Document
from pptx import Presentation

from app.schemas.document import ExtractedUnit


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".pptx"}


class DocumentExtractionError(Exception):
    """Raised when a document cannot be extracted."""


def extract_pdf(file_path: Path) -> list[ExtractedUnit]:
    """Extract text from PDF pages."""

    extracted = []

    with pymupdf.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            if text:
                extracted.append(
                    ExtractedUnit(
                        text=text,
                        metadata={
                            "source": file_path.name,
                            "file_type": "pdf",
                            "page_number": page_number,
                        },
                    )
                )

    return extracted


def extract_docx(file_path: Path) -> list[ExtractedUnit]:
    """Extract paragraphs and tables from a Word document."""

    document = Document(file_path)
    content = []

    # Extract paragraphs
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            content.append(text)

    # Extract tables
    for table in document.tables:
        for row in table.rows:
            cells = [
                cell.text.strip()
                for cell in row.cells
            ]

            row_text = " | ".join(
                cell for cell in cells if cell
            )

            if row_text:
                content.append(row_text)

    full_text = "\n".join(content).strip()

    if not full_text:
        return []

    return [
        ExtractedUnit(
            text=full_text,
            metadata={
                "source": file_path.name,
                "file_type": "docx",
            },
        )
    ]


def extract_pptx(file_path: Path) -> list[ExtractedUnit]:
    """Extract text from PowerPoint slides."""

    presentation = Presentation(file_path)
    extracted = []

    for slide_number, slide in enumerate(
        presentation.slides, start=1
    ):
        slide_content = []

        for shape in slide.shapes:

            if shape.has_text_frame:
                text = shape.text.strip()

                if text:
                    slide_content.append(text)

            if shape.has_table:
                for row in shape.table.rows:
                    cells = [
                        cell.text.strip()
                        for cell in row.cells
                    ]

                    row_text = " | ".join(
                        cell for cell in cells if cell
                    )

                    if row_text:
                        slide_content.append(row_text)

        full_text = "\n".join(slide_content).strip()

        if full_text:
            extracted.append(
                ExtractedUnit(
                    text=full_text,
                    metadata={
                        "source": file_path.name,
                        "file_type": "pptx",
                        "slide_number": slide_number,
                    },
                )
            )

    return extracted


def extract_text_file(file_path: Path) -> list[ExtractedUnit]:
    """Extract text from TXT or Markdown files."""

    text = file_path.read_text(
        encoding="utf-8-sig",
        errors="replace",
    ).strip()

    if not text:
        return []

    return [
        ExtractedUnit(
            text=text,
            metadata={
                "source": file_path.name,
                "file_type": file_path.suffix.lower().lstrip("."),
            },
        )
    ]


def extract_document(file_path: Path) -> list[ExtractedUnit]:
    """
    Extract text from a supported document.

    Returns a list of text units with source metadata.
    """

    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise DocumentExtractionError(
            f"Unsupported file format: {extension}"
        )

    if not file_path.is_file():
        raise DocumentExtractionError(
            "Document does not exist."
        )

    try:
        if extension == ".pdf":
            extracted = extract_pdf(file_path)

        elif extension == ".docx":
            extracted = extract_docx(file_path)

        elif extension == ".pptx":
            extracted = extract_pptx(file_path)

        else:
            extracted = extract_text_file(file_path)

    except DocumentExtractionError:
        raise

    except Exception as exc:
        raise DocumentExtractionError(
            f"Failed to extract {file_path.name}: {exc}"
        ) from exc

    if not extracted:
        raise DocumentExtractionError(
            f"No extractable text found in {file_path.name}."
        )

    return extracted
