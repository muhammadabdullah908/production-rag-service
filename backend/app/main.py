from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import documents, ask

app = FastAPI(title="Production RAG Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api")
app.include_router(ask.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}