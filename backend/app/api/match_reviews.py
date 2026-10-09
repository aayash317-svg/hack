from datetime import datetime, timezone
import secrets
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.complaint import Complaint
from backend.app.models.case_link import CaseLink
from backend.app.models.case_group import CaseGroup, CaseGroupMember
from backend.app.schemas.review import (
    MatchReviewItem,
    MatchReviewCandidate,
    MatchDecisionRequest
)
from backend.app.core.permissions import require_roles
from backend.app.services.escalation_service import EscalationService
from backend.app.services.audit_service import AuditService

router = APIRouter(prefix="", tags=["Match Reviews"])


@router.get("/authority/match-reviews", response_model=List[MatchReviewItem])
def list_pending_match_reviews(
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """
    Lists candidate related reports flagged for human review.
    Displays side-by-side incident details without exposing reporter identities.
    """
    links = db.query(CaseLink).filter(CaseLink.review_status == "pending").all()
    results: List[MatchReviewItem] = []

    for link in links:
        cA = db.query(Complaint).filter(Complaint.id == link.complaint_id).first()
        cB = db.query(Complaint).filter(Complaint.id == link.related_complaint_id).first()

        if not cA or not cB:
            continue

        suspect_a = ", ".join([f"{s.name or 'Unknown'} ({s.department or 'N/A'})" for s in cA.suspect_details]) or None
        suspect_b = ", ".join([f"{s.name or 'Unknown'} ({s.department or 'N/A'})" for s in cB.suspect_details]) or None

        cand_a = MatchReviewCandidate(
            id=cA.id,
            public_reference=cA.public_reference,
            type=cA.type,
            category=cA.category,
            incident_date=cA.incident_date,
            location_or_platform=cA.location_or_platform,
            description=cA.description,
            suspect_summary=suspect_a
        )
        cand_b = MatchReviewCandidate(
            id=cB.id,
            public_reference=cB.public_reference,
            type=cB.type,
            category=cB.category,
            incident_date=cB.incident_date,
            location_or_platform=cB.location_or_platform,
            description=cB.description,
            suspect_summary=suspect_b
        )

        features = [r.strip() for r in (link.reason or "Algorithm similarity match").split(";")]

        results.append(
            MatchReviewItem(
                link_id=link.id,
                complaint_a=cand_a,
                complaint_b=cand_b,
                matched_features=features,
                created_at=link.created_at
            )
        )

    return results


@router.post("/cases/match-reviews/{link_id}/decide")
def decide_match_review(
    link_id: int,
    decision_in: MatchDecisionRequest,
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """
    Records an authorized human review decision for a candidate match link.
    Per Section 23:
    - 'confirm': links complaints into a case_group and recalculates escalation count.
    - 'reject' / 'needs_more_review': preserves independent cases and never increases repeat count.
    """
    link = db.query(CaseLink).filter(CaseLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Match link not found.")

    link.review_status = decision_in.decision
    link.reviewed_by = current_user.id
    link.reviewed_at = datetime.now(timezone.utc)
    link.reason = decision_in.reason

    cA = db.query(Complaint).filter(Complaint.id == link.complaint_id).first()
    cB = db.query(Complaint).filter(Complaint.id == link.related_complaint_id).first()

    group_id = None
    if decision_in.decision == "confirm":
        # Check existing group membership for either complaint
        member_a = db.query(CaseGroupMember).filter(CaseGroupMember.complaint_id == link.complaint_id).first()
        member_b = db.query(CaseGroupMember).filter(CaseGroupMember.complaint_id == link.related_complaint_id).first()

        if member_a:
            group_id = member_a.case_group_id
        elif member_b:
            group_id = member_b.case_group_id
        else:
            # Create a brand new case group
            group_ref = f"GRP-{datetime.now().year}-{secrets.token_hex(3).upper()}"
            new_group = CaseGroup(
                group_reference=group_ref,
                created_by=current_user.id,
                status="active"
            )
            db.add(new_group)
            db.flush()
            group_id = new_group.id

        # Ensure both complaints are in the group
        for cid in [link.complaint_id, link.related_complaint_id]:
            existing_mem = db.query(CaseGroupMember).filter(
                CaseGroupMember.case_group_id == group_id,
                CaseGroupMember.complaint_id == cid
            ).first()
            if not existing_mem:
                db.add(CaseGroupMember(case_group_id=group_id, complaint_id=cid))

        db.flush()

        # Update complaints out of pending_match_review
        if cA and cA.status == "pending_match_review":
            cA.status = "under_review"
        if cB and cB.status == "pending_match_review":
            cB.status = "under_review"

        # Apply Section 23 repeat-report escalation engine
        EscalationService.evaluate_group_escalation(
            db=db,
            case_group_id=group_id,
            reason=f"Confirmed related pattern by {current_user.name}: {decision_in.reason}"
        )
    else:
        # If rejected or needs_more_review, return complaints to under_review if they were pending review
        if cA and cA.status == "pending_match_review":
            cA.status = "under_review"
        if cB and cB.status == "pending_match_review":
            cB.status = "under_review"

    AuditService.log_event(
        db=db,
        actor_user_id=current_user.id,
        action="MATCH_REVIEW_DECISION",
        resource_type="case_link",
        resource_id=str(link.id),
        reason=f"Decision: {decision_in.decision}. Justification: {decision_in.reason}"
    )

    db.commit()
    return {
        "message": f"Match review decision '{decision_in.decision}' recorded successfully.",
        "case_group_id": group_id
    }
