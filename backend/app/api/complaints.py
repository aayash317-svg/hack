from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.schemas.complaint import ComplaintCreate, ComplaintSubmissionResponse
from backend.app.services.complaint_service import ComplaintService
from backend.app.core.config import settings

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.post("", response_model=ComplaintSubmissionResponse, status_code=status.HTTP_201_CREATED)
def submit_complaint(
    complaint_in: ComplaintCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Submits a confidential or anonymous complaint.
    - Generates high-entropy tracking credentials.
    - Keeps reporter identity isolated in reporter_identities table if confidential.
    - Zero identity records created if anonymous.
    """
    client_ip = request.client.host if request.client else None
    complaint, tracking_secret = ComplaintService.create_complaint(
        db=db,
        complaint_in=complaint_in,
        client_ip=client_ip
    )

    urgent_guidance = None
    if complaint.is_urgent:
        urgent_guidance = (
            f"URGENT ALERT RECORDED: For immediate safety, contact {settings.INSTITUTION_NAME} "
            f"Helpline at {settings.EMERGENCY_HELPLINE} or visit {settings.SECURITY_GATE_CONTACT}."
        )

    return ComplaintSubmissionResponse(
        public_reference=complaint.public_reference,
        tracking_secret=tracking_secret,
        status=complaint.status,
        reporting_mode=complaint.reporting_mode,
        is_urgent=complaint.is_urgent,
        created_at=complaint.created_at,
        message="Your report has been securely registered. Keep your tracking secret safe; it cannot be recovered.",
        urgent_guidance=urgent_guidance
    )
