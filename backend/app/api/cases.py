from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.complaint import Complaint
from backend.app.models.identity import ReporterIdentity
from backend.app.models.status_history import CaseStatusHistory
from backend.app.models.case_group import CaseGroupMember, CaseGroup
from backend.app.models.escalation import Escalation
from backend.app.schemas.case import (
    CaseListItem,
    CaseDetailResponse,
    SuspectDetailResponse,
    EvidenceResponse,
    StatusHistoryResponse,
    StatusUpdateRequest,
    UnmaskedIdentityResponse,
    RequestIdentityAccess
)
from backend.app.core.permissions import require_roles
from backend.app.services.audit_service import AuditService

router = APIRouter(prefix="/cases", tags=["Authority Cases"])


@router.get("", response_model=List[CaseListItem])
def list_cases(
    status_filter: Optional[str] = Query(None, alias="status"),
    urgent_only: Optional[bool] = Query(None, alias="urgent"),
    type_filter: Optional[str] = Query(None, alias="type"),
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """
    Returns case list for authorized authority dashboard.
    Strictly excludes reporter identity fields.
    """
    query = db.query(Complaint)

    if status_filter:
        query = query.filter(Complaint.status == status_filter)
    if urgent_only:
        query = query.filter(Complaint.is_urgent == True)
    if type_filter:
        query = query.filter(Complaint.type == type_filter)

    complaints = query.order_by(desc(Complaint.created_at)).all()

    items: List[CaseListItem] = []
    for c in complaints:
        # Check if in a case group
        group_member = db.query(CaseGroupMember).filter(CaseGroupMember.complaint_id == c.id).first()
        group_id = None
        group_ref = None
        group_count = 1

        if group_member:
            group_id = group_member.case_group_id
            group = db.query(CaseGroup).filter(CaseGroup.id == group_id).first()
            if group:
                group_ref = group.group_reference
            group_count = db.query(CaseGroupMember).filter(CaseGroupMember.case_group_id == group_id).count()

        items.append(
            CaseListItem(
                id=c.id,
                public_reference=c.public_reference,
                reporting_mode=c.reporting_mode,
                type=c.type,
                category=c.category,
                incident_date=c.incident_date,
                location_or_platform=c.location_or_platform,
                is_urgent=c.is_urgent,
                status=c.status,
                created_at=c.created_at,
                case_group_id=group_id,
                group_reference=group_ref,
                confirmed_reports_in_group=group_count
            )
        )

    return items


@router.get("/{case_id}", response_model=CaseDetailResponse)
def get_case_detail(
    case_id: int,
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """
    Retrieves full incident details for an assigned case.
    Reporter identity remains redacted by default.
    """
    complaint = db.query(Complaint).filter(Complaint.id == case_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Case not found.")

    # Check case group & confirmed count
    group_member = db.query(CaseGroupMember).filter(CaseGroupMember.complaint_id == complaint.id).first()
    group_id = None
    group_ref = None
    group_count = 1
    current_level = 1

    if group_member:
        group_id = group_member.case_group_id
        group = db.query(CaseGroup).filter(CaseGroup.id == group_id).first()
        if group:
            group_ref = group.group_reference
        group_count = db.query(CaseGroupMember).filter(CaseGroupMember.case_group_id == group_id).count()
        latest_esc = db.query(Escalation).filter(Escalation.case_group_id == group_id).order_by(desc(Escalation.level)).first()
        if latest_esc:
            current_level = latest_esc.level
    else:
        latest_esc = db.query(Escalation).filter(Escalation.complaint_id == complaint.id).order_by(desc(Escalation.level)).first()
        if latest_esc:
            current_level = latest_esc.level

    suspects = [
        SuspectDetailResponse(
            id=s.id,
            name=s.name,
            department=s.department,
            phone=s.phone,
            other_description=s.other_description
        )
        for s in complaint.suspect_details
    ]

    evidence_list = [
        EvidenceResponse(
            id=e.id,
            original_filename_display=e.original_filename_display,
            verified_media_type=e.verified_media_type,
            file_size=e.file_size,
            uploaded_at=e.uploaded_at
        )
        for e in complaint.evidence_items
    ]

    histories = [
        StatusHistoryResponse(
            id=h.id,
            previous_status=h.previous_status,
            new_status=h.new_status,
            changed_by_name=None,
            reason=h.reason,
            created_at=h.created_at
        )
        for h in complaint.status_history
    ]

    has_identity = bool(complaint.reporter_identity is not None)

    return CaseDetailResponse(
        id=complaint.id,
        public_reference=complaint.public_reference,
        reporting_mode=complaint.reporting_mode,
        type=complaint.type,
        category=complaint.category,
        incident_date=complaint.incident_date,
        incident_time=complaint.incident_time,
        location_or_platform=complaint.location_or_platform,
        description=complaint.description,
        is_urgent=complaint.is_urgent,
        status=complaint.status,
        created_at=complaint.created_at,
        updated_at=complaint.updated_at,
        suspect_details=suspects,
        evidence_items=evidence_list,
        status_history=histories,
        case_group_id=group_id,
        group_reference=group_ref,
        confirmed_reports_in_group=group_count,
        current_escalation_level=current_level,
        has_confidential_identity=has_identity,
        unmasked_identity=None  # Concealed by default
    )


@router.patch("/{case_id}/status")
def update_case_status(
    case_id: int,
    update_data: StatusUpdateRequest,
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """Updates permitted case status and records status history and audit log."""
    complaint = db.query(Complaint).filter(Complaint.id == case_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Case not found.")

    prev_status = complaint.status
    complaint.status = update_data.new_status

    history = CaseStatusHistory(
        complaint_id=complaint.id,
        previous_status=prev_status,
        new_status=update_data.new_status,
        changed_by=current_user.id,
        reason=update_data.reason
    )
    db.add(history)

    AuditService.log_event(
        db=db,
        actor_user_id=current_user.id,
        action="STATUS_CHANGE",
        resource_type="complaint",
        resource_id=complaint.public_reference,
        reason=f"From {prev_status} to {update_data.new_status}: {update_data.reason}"
    )

    db.commit()
    return {"message": "Status updated successfully.", "status": complaint.status}


@router.post("/{case_id}/request-identity", response_model=UnmaskedIdentityResponse)
def request_identity_access(
    case_id: int,
    req: RequestIdentityAccess,
    request: Request,
    current_user: User = Depends(require_roles(["hod", "dean", "higher_authority", "administrator"])),
    db: Session = Depends(get_db)
):
    """
    Exceptional identity access endpoint.
    Strictly restricted to cases with confidential mode; logs an immediate high-priority audit record.
    """
    complaint = db.query(Complaint).filter(Complaint.id == case_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Case not found.")

    if complaint.reporting_mode == "anonymous" or not complaint.reporter_identity:
        raise HTTPException(
            status_code=400,
            detail="Cannot unmask identity: This report was submitted anonymously. Zero identity records exist."
        )

    identity = complaint.reporter_identity

    # Mandatory security audit log
    AuditService.log_event(
        db=db,
        actor_user_id=current_user.id,
        action="IDENTITY_UNMASKED",
        resource_type="reporter_identity",
        resource_id=complaint.public_reference,
        reason=f"Official clearance granted. Stated justification: {req.justified_reason}",
        ip_address=request.client.host if request.client else None
    )
    db.commit()

    return UnmaskedIdentityResponse(
        full_name=identity.full_name,
        email=identity.email,
        phone=identity.phone,
        department=identity.department,
        student_id_number=identity.student_id_number,
        access_policy=identity.access_policy
    )
