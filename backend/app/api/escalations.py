from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.complaint import Complaint
from backend.app.models.escalation import Escalation
from backend.app.models.case_group import CaseGroupMember
from backend.app.schemas.case import EscalateRequest
from backend.app.core.permissions import require_roles
from backend.app.services.escalation_service import EscalationService

router = APIRouter(prefix="", tags=["Escalations"])


@router.post("/cases/{case_id}/escalate")
def escalate_case_manual(
    case_id: int,
    req: EscalateRequest,
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """Manually escalates a case to a specified level (HOD -> Dean -> Higher Authority)."""
    complaint = db.query(Complaint).filter(Complaint.id == case_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found.")

    escalation = EscalationService.escalate_single_complaint(
        db=db,
        complaint=complaint,
        target_level=req.target_level,
        reason=f"Manual escalation by {current_user.name} ({current_user.role}): {req.reason}",
        actor_id=current_user.id
    )
    db.commit()

    return {
        "message": f"Case escalated to Level {req.target_level} successfully.",
        "escalation_id": escalation.id,
        "status": complaint.status
    }


@router.get("/cases/{case_id}/escalations")
def get_case_escalations(
    case_id: int,
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """Retrieves escalation history for a case."""
    complaint = db.query(Complaint).filter(Complaint.id == case_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found.")

    member = db.query(CaseGroupMember).filter(CaseGroupMember.complaint_id == case_id).first()
    group_id = member.case_group_id if member else None

    escalations = db.query(Escalation).filter(
        or_(
            Escalation.complaint_id == case_id,
            Escalation.case_group_id == group_id if group_id else False
        )
    ).order_by(Escalation.created_at.desc()).all()

    return [
        {
            "id": e.id,
            "level": e.level,
            "reason": e.reason,
            "status": e.status,
            "created_at": e.created_at
        }
        for e in escalations
    ]
