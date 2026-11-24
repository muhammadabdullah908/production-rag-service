
from pathlib import Path

from docx import Document
from pptx import Presentation
from pptx.util import Inches

import pymupdf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample_documents"

SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


# 1. Create PDF
pdf_path = SAMPLE_DIR / "ai_notes.pdf"

pdf = pymupdf.open()
page = pdf.new_page()
page.insert_text(
    (72, 72),
    "Artificial Intelligence is transforming the world.\n"
    "Machine Learning enables computers to learn from data.\n"
    "Deep Learning uses neural networks.",
    fontsize=12,
)
pdf.save(pdf_path)
pdf.close()


# 2. Create DOCX
docx_path = SAMPLE_DIR / "ai_notes.docx"

document = Document()
document.add_heading("Artificial Intelligence Notes", level=1)
document.add_paragraph(
    "Artificial Intelligence is a field of computer science."
)
document.add_paragraph(
    "Machine Learning is a subset of Artificial Intelligence."
)
document.add_paragraph(
    "Deep Learning uses neural networks."
)

document.save(docx_path)


# 3. Create PPTX
pptx_path = SAMPLE_DIR / "ai_notes.pptx"

presentation = Presentation()
slide = presentation.slides.add_slide(
    presentation.slide_layouts[1]
)

slide.shapes.title.text = "Artificial Intelligence"

slide.placeholders[1].text = (
    "Machine Learning learns from data.\n"
    "Deep Learning uses neural networks."
)

presentation.save(pptx_path)


print("Sample documents created successfully!")

for file_path in SAMPLE_DIR.iterdir():
    print(file_path.name)
