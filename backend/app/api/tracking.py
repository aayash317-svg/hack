from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.models.complaint import Complaint
from backend.app.schemas.tracking import TrackingResponse, MilestoneItem
from backend.app.core.security import verify_tracking_secret

router = APIRouter(prefix="/complaints", tags=["Tracking"])


@router.get("/track", response_model=TrackingResponse)
def track_complaint(
    reference: str = Query(..., description="Public reference code, e.g., REF-2026-XXXX"),
    secret: str = Query(..., description="Private tracking secret, e.g., TRK-..."),
    db: Session = Depends(get_db)
):
    """
    Checks the status of a submitted report using its public reference and tracking secret.
    Returns sanitized public milestone progress only. Internal notes, suspect allegations,
    and reporter identities are never returned.
    """
    complaint = db.query(Complaint).filter(Complaint.public_reference == reference.strip()).first()
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No complaint found matching the provided reference."
        )

    # Verify secret hash
    if not verify_tracking_secret(secret.strip(), complaint.tracking_secret_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid tracking secret for this reference."
        )

    # Construct public milestone timeline
    milestones: list[MilestoneItem] = []
    # 1. Submitted milestone
    milestones.append(
        MilestoneItem(
            status="submitted",
            label="Report Registered",
            timestamp=complaint.created_at,
            description="Your report was safely received by the system."
        )
    )

    # 2. Subsequent status transitions from history
    for h in sorted(complaint.status_history, key=lambda x: x.created_at):
        if h.new_status != "submitted":
            label_map = {
                "under_review": "Under Review",
                "pending_match_review": "Pattern Assessment",
                "escalated": "Escalated for Action",
                "awaiting_information": "Awaiting Details",
                "resolved": "Resolution Issued",
                "closed": "Case Closed"
            }
            desc_map = {
                "under_review": "Designated authority has acknowledged and begun case review.",
                "pending_match_review": "Case is undergoing institutional review for related safety patterns.",
                "escalated": "Case has been routed to senior administration for intervention.",
                "awaiting_information": "Additional information may be requested if a contact channel exists.",
                "resolved": "Corrective action or support measure has been implemented.",
                "closed": "Formal review cycle has concluded."
            }
            milestones.append(
                MilestoneItem(
                    status=h.new_status,
                    label=label_map.get(h.new_status, h.new_status.replace("_", " ").title()),
                    timestamp=h.created_at,
                    description=desc_map.get(h.new_status, "Status updated by authorized staff.")
                )
            )

    public_msg = (
        "Thank you for reporting. Your case is actively monitored in accordance with "
        "campus anti-ragging and safety protocols."
    )
    if complaint.status in ["resolved", "closed"]:
        public_msg = "This case has reached its documented resolution. If you experience further issues, please reach out."

    return TrackingResponse(
        public_reference=complaint.public_reference,
        reporting_mode=complaint.reporting_mode,
        status=complaint.status,
        category=complaint.category,
        type=complaint.type,
        incident_date=complaint.incident_date,
        is_urgent=complaint.is_urgent,
        created_at=complaint.created_at,
        timeline=milestones,
        public_message=public_msg
    )
