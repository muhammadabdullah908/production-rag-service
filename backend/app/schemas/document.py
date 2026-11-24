
from pydantic import BaseModel, Field


class ExtractedUnit(BaseModel):
    """A piece of extracted text with its source metadata."""

    text: str = Field(min_length=1)
    metadata: dict[str, str | int] = Field(default_factory=dict)
