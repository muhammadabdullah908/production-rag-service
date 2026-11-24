
from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="Production RAG Service",
    description="A document-based Retrieval-Augmented Generation API",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Welcome endpoint."""
    return {
        "message": "Welcome to Production RAG Service!",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Check whether the backend is healthy."""
    return {
        "status": "healthy",
        "service": "Production RAG Service",
    }
