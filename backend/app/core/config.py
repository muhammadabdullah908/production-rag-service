"""Central configuration. All secrets come from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env (never hard-coded)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM (Groq — free tier, no credit card)
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"

    # Embeddings (local, no API key)
    embedding_model: str = "all-MiniLM-L6-v2"

    # Vector store
    chroma_path: str = "./data/chroma"

    # Chunking
    chunk_size: int = 800
    chunk_overlap: int = 150

    # Retrieval
    top_k: int = 5
    similarity_threshold: float = 0.0

    # Ingestion
    max_file_size_mb: int = 50
    allowed_extensions: tuple[str, ...] = ("pdf", "docx", "pptx", "txt", "md")


settings = Settings()