
"""Central configuration. All secrets come from environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Locate the project root:
# config.py -> core -> app -> backend -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """Application settings loaded from the project-root .env."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-20b"

    # Embeddings
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
    allowed_extensions: tuple[str, ...] = (
        "pdf", "docx", "pptx", "txt", "md"
    )


settings = Settings()
