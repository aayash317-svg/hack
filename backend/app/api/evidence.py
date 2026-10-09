from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.complaint import Complaint
from backend.app.models.evidence import Evidence
from backend.app.schemas.case import EvidenceResponse
from backend.app.core.permissions import require_roles
from backend.app.services.evidence_service import EvidenceService
from backend.app.services.audit_service import AuditService

router = APIRouter(prefix="", tags=["Evidence Storage"])


@router.post("/cases/{case_id}/evidence", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
async def upload_case_evidence(
    case_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Uploads an evidence file linked to a complaint, saving it in private disk storage."""
    complaint = db.query(Complaint).filter(Complaint.id == case_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found.")

    evidence = await EvidenceService.save_evidence_file(db, complaint.id, file)

    AuditService.log_event(
        db=db,
        action="EVIDENCE_UPLOADED",
        resource_type="evidence",
        resource_id=str(evidence.id),
        reason=f"File: {evidence.original_filename_display} ({evidence.file_size} bytes)"
    )

    db.commit()
    db.refresh(evidence)

    return EvidenceResponse(
        id=evidence.id,
        original_filename_display=evidence.original_filename_display,
        verified_media_type=evidence.verified_media_type,
        file_size=evidence.file_size,
        uploaded_at=evidence.uploaded_at
    )


@router.get("/evidence/{evidence_id}")
def download_evidence(
    evidence_id: int,
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """
    Downloads or previews privately stored evidence.
    Enforces server-side authorization on every request and logs audit access.
    """
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found.")

    file_path = EvidenceService.get_evidence_filepath(evidence.storage_key)

    AuditService.log_event(
        db=db,
        actor_user_id=current_user.id,
        action="EVIDENCE_ACCESSED",
        resource_type="evidence",
        resource_id=str(evidence.id),
        reason=f"Accessed by {current_user.name} ({current_user.role})"
    )
    db.commit()

    return FileResponse(
        path=str(file_path),
        media_type=evidence.verified_media_type,
        filename=evidence.original_filename_display
    )
