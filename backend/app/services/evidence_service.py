import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.models.evidence import Evidence


class EvidenceService:
    @staticmethod
    def ensure_storage_dir():
        storage_path = Path(settings.EVIDENCE_STORAGE_DIR)
        storage_path.mkdir(parents=True, exist_ok=True)
        return storage_path

    @classmethod
    async def save_evidence_file(
        cls,
        db: Session,
        complaint_id: int,
        file: UploadFile
    ) -> Evidence:
        """Validates and stores an evidence file privately on disk."""
        # Validate media type
        if file.content_type not in settings.ALLOWED_MEDIA_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{file.content_type}'. Allowed types: PNG, JPEG, PDF."
            )

        # Read file bytes & check size
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=f"File exceeds maximum size limit of {settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)} MB."
            )

        storage_path = cls.ensure_storage_dir()
        storage_key = f"{uuid.uuid4().hex}.dat"
        file_disk_path = storage_path / storage_key

        with open(file_disk_path, "wb") as f:
            f.write(content)

        evidence = Evidence(
            complaint_id=complaint_id,
            storage_key=storage_key,
            original_filename_display=file.filename or "attachment",
            verified_media_type=file.content_type,
            file_size=len(content)
        )
        db.add(evidence)
        db.flush()
        return evidence

    @classmethod
    def get_evidence_filepath(cls, storage_key: str) -> Path:
        """Returns the absolute file path for an authorized evidence download."""
        storage_path = cls.ensure_storage_dir()
        file_path = storage_path / storage_key
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Evidence file not found on disk.")
        return file_path
