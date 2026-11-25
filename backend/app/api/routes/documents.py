
import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.core.config import settings
from app.services.ingest_service import (
    ingest_file,
    list_documents,
    delete_document,
    DuplicateDocumentError,
    UnsupportedFileError,
    EmptyDocumentError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    """Upload and ingest a supported document, enforcing the configured size limit."""

    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    allowed_extensions = {
        f".{ext.lower().lstrip('.')}"
        for ext in settings.allowed_extensions
    }

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file format.",
        )

    max_bytes = settings.max_file_size_mb * 1024 * 1024
    temp_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{extension}"
    total_bytes = 0

    try:
        # Read in small blocks so oversized uploads are rejected before
        # the entire file is written to disk.
        with temp_path.open("wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_bytes += len(chunk)

                if total_bytes > max_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File exceeds the {settings.max_file_size_mb} MB upload limit.",
                    )

                buffer.write(chunk)

        if total_bytes == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is empty.",
            )

        return ingest_file(temp_path)

    except UnsupportedFileError:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file format.",
        )
    except DuplicateDocumentError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    except EmptyDocumentError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Document ingestion failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document ingestion failed. Check the server logs for details.",
        )
    finally:
        if temp_path.exists():
            temp_path.unlink()
        await file.close()


@router.get("")
async def get_documents():
    """List all uploaded documents."""
    return list_documents()


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doc(doc_id: str):
    """Delete a document and all its vectors."""
    delete_document(doc_id)
    return None
