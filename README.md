@'
# Production RAG Service

A document-based Retrieval-Augmented Generation application built with FastAPI, ChromaDB, ONNX MiniLM embeddings, and the Groq API.

## Features
- Upload PDF, DOCX, PPTX, TXT, and Markdown files.
- Extract and chunk document text.
- Detect duplicate files using SHA-256 hashes.
- Generate local embeddings and store them in persistent ChromaDB.
- Ask questions and generate answers grounded in retrieved document context.
- Inspect retrieved chunks and scores.
- List and delete uploaded documents.
- Refuse questions that cannot be answered from available context.

## Technology
- Python 3.13, FastAPI
- Groq API: openai/gpt-oss-20b
- ONNX MiniLM: all-MiniLM-L6-v2
- ChromaDB
- PyMuPDF, python-docx, python-pptx
- HTML, CSS, JavaScript
- pytest

## Setup
1. Create a virtual environment: `python -m venv .venv`
2. Activate it: `.\.venv\Scripts\Activate.ps1`
3. Install dependencies: `python -m pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your Groq API key.

Never commit `.env` or expose your API key.

## Run the Backend
From the project root:
`cd backend`
`python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001`

## Run the Frontend
In a second terminal:
`cd frontend`
`python -m http.server 5500 --bind 127.0.0.1`

Open http://127.0.0.1:5500.
API documentation: http://127.0.0.1:8001/docs.

## API
- POST /api/documents — upload a document
- GET /api/documents — list documents
- DELETE /api/documents/{doc_id} — delete a document
- POST /api/ask — ask a question

## Tests and Evaluation
Run tests: `python -m pytest .\backend\tests -v`

With the backend running, evaluate: `python .\evals\run_eval.py`

See EVAL.md for results and DESIGN.md for architecture.

## Limitations
This is a portfolio prototype, not a fully hardened production deployment. Authentication, per-user isolation, OCR, comprehensive file-content validation, and deployment-level request limits are not implemented. Evaluation results are based on a small automated dataset and do not establish human-judged answer quality.
'@ | Set-Content -Encoding utf8 .\README.md