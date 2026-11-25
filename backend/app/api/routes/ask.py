from fastapi import APIRouter, HTTPException, status
from app.schemas.chat import AskRequest, AskResponse, ChunkResult
from app.retrieval.retriever import retrieve_context
from app.rag.generation import LLMServiceError, generate_answer

router = APIRouter(prefix="/ask", tags=["QA"])

@router.post("", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """Ask a question based on the uploaded documents."""
    try:
        chunks = retrieve_context(request.question)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Document retrieval is unavailable. Try again.",
        ) from e

    try:
        answer = generate_answer(request.question, chunks)
    except LLMServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        ) from e

    formatted_chunks = [
        ChunkResult(
            text=c["text"],
            score=c["score"],
            file_name=c["metadata"].get("file_name", "Unknown"),
            page_number=c["metadata"].get("page_number")
        ) for c in chunks
    ]

    return AskResponse(answer=answer, retrieved_chunks=formatted_chunks)