from pydantic import BaseModel, Field
from typing import List

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000, description="The question to ask")

class ChunkResult(BaseModel):
    text: str
    score: float
    file_name: str
    page_number: int | None = None

class AskResponse(BaseModel):
    answer: str
    retrieved_chunks: List[ChunkResult]