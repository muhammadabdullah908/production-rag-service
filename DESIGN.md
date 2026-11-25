@'
# System Design

## Overview
This project implements Retrieval-Augmented Generation (RAG). Uploaded documents are indexed, relevant passages are retrieved for each question, and those passages are supplied to a language model to generate grounded answers.

## Architecture
- Frontend: HTML, CSS, and JavaScript.
- API: FastAPI.
- Extraction: PyMuPDF, python-docx, and python-pptx, with TXT and Markdown support.
- Chunking: approximately 800 characters with 150 characters of overlap.
- Embeddings: local ONNX all-MiniLM-L6-v2.
- Vector storage: persistent ChromaDB.
- Generation: Groq API using openai/gpt-oss-20b.

## Ingestion Workflow
1. User uploads a supported document.
2. API checks file extension and configured size limit.
3. Ingestion service calculates a SHA-256 hash for duplicate detection.
4. Extractor reads document text.
5. Chunker creates overlapping text chunks.
6. Embedding model converts chunks into vectors.
7. ChromaDB stores vectors, text, and metadata.
8. Temporary upload file is removed.

## Question-Answering Workflow
1. User submits a question.
2. The question is embedded.
3. ChromaDB retrieves the top matching chunks.
4. Retrieved context is passed to the generation service.
5. The Groq model generates a context-grounded response.
6. API returns the answer and retrieved chunk details.

## Design Decisions
- Local ONNX embeddings avoid a separate paid embedding API.
- Persistent ChromaDB retains indexed data between runs.
- Overlapping chunks help preserve context at chunk boundaries.
- Returning retrieved chunks and scores makes retrieval inspectable.
- Separate ingestion, retrieval, and generation modules improve maintainability.

## Security and Limitations
Secrets are configured through environment variables. The frontend uses safe DOM text methods rather than injecting untrusted content through innerHTML. Upload checks are implemented at the application level.

This is a portfolio prototype, not a hardened production service. Authentication, authorization, per-user isolation, content-signature validation, deployment-level request limits, monitoring, and additional security testing remain future work.

## Evaluation
See EVAL.md for the golden dataset results and evaluation methodology.
'@ | Set-Content -Encoding utf8 .\DESIGN.md