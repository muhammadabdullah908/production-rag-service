import logging
from groq import APIConnectionError, APIStatusError, Groq
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMServiceError(RuntimeError):
    """Raised when the Groq service cannot complete a request."""


SYSTEM_PROMPT = """You are a helpful AI assistant answering questions based on the provided documents.
You MUST follow these rules:
1. Answer the question using ONLY the provided context.
2. If the context does not contain the answer, say "I cannot answer this based on the provided documents."
3. Cite your sources using [1], [2], etc., corresponding to the source number provided in the context.
4. Do not make up facts.
"""

def generate_answer(question: str, chunks: list[dict]) -> str:
    """Generate a grounded answer using Groq."""
    if not chunks:
        return "I cannot answer this based on the provided documents."
    if not settings.groq_api_key.strip():
        raise LLMServiceError("Groq API key is not configured.")

    # Build context string with citation numbers
    context_str = ""
    for i, chunk in enumerate(chunks):
        source = chunk['metadata'].get('file_name', 'Unknown')
        page = chunk['metadata'].get('page_number', '')
        page_str = f" (Page {page})" if page else ""
        context_str += f"\n[{i+1}] Source: {source}{page_str}\n{chunk['text']}\n"

    user_prompt = f"Context:\n{context_str}\n\nQuestion: {question}\n\nAnswer:"

    try:
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
    model=settings.groq_model,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ],
    max_completion_tokens=500,
)
        return response.choices[0].message.content.strip()
    except APIConnectionError as e:
        cause = e.__cause__
        cause_detail = f"{type(cause).__name__}: {cause}" if cause else "unknown cause"
        logger.error("Groq API connection failed (%s)", cause_detail)
        raise LLMServiceError(
            "Could not connect to Groq. Check network access and try again."
        ) from e
    except APIStatusError as e:
        logger.error("Groq API returned HTTP %d", e.status_code)
        raise LLMServiceError(
            f"Groq API returned HTTP {e.status_code}. Check the API key, model, or account limits."
        ) from e

    except Exception:
        logger.exception("Unexpected error while generating answer with Groq")
    raise LLMServiceError(
            "An unexpected error occurred while generating the answer."
        )