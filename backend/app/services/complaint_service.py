from typing import Tuple, Optional
from sqlalchemy.orm import Session
from backend.app.schemas.complaint import ComplaintCreate
from backend.app.models.complaint import Complaint
from backend.app.models.identity import ReporterIdentity
from backend.app.models.suspect import SuspectDetail
from backend.app.models.status_history import CaseStatusHistory
from backend.app.core.security import (
    generate_public_reference,
    generate_tracking_secret,
    hash_tracking_secret
)
from backend.app.services.matching_service import MatchingService
from backend.app.services.escalation_service import EscalationService
from backend.app.services.audit_service import AuditService


class ComplaintService:
    @classmethod
    def create_complaint(
        cls,
        db: Session,
        complaint_in: ComplaintCreate,
        client_ip: Optional[str] = None
    ) -> Tuple[Complaint, str]:
        """
        Creates a new complaint.
        - Strict separation: reporter identity is saved only in reporter_identities table if confidential.
        - Anonymous mode never writes to reporter_identities.
        - Tracking secret is hashed before persistence; plaintext returned only once to caller.
        """
        public_ref = generate_public_reference()
        raw_tracking_secret = generate_tracking_secret()
        secret_hash = hash_tracking_secret(raw_tracking_secret)

        complaint = Complaint(
            public_reference=public_ref,
            tracking_secret_hash=secret_hash,
            reporting_mode=complaint_in.reporting_mode,
            type=complaint_in.type,
            category=complaint_in.category,
            incident_date=complaint_in.incident_date,
            incident_time=complaint_in.incident_time,
            location_or_platform=complaint_in.location_or_platform,
            description=complaint_in.description,
            is_urgent=complaint_in.is_urgent,
            status="submitted"
        )
        db.add(complaint)
        db.flush()

        # Handle Confidential Identity Isolation
        if complaint_in.reporting_mode == "confidential" and complaint_in.reporter_identity:
            identity = ReporterIdentity(
                complaint_id=complaint.id,
                full_name=complaint_in.reporter_identity.full_name,
                email=complaint_in.reporter_identity.email,
                phone=complaint_in.reporter_identity.phone,
                department=complaint_in.reporter_identity.department,
                student_id_number=complaint_in.reporter_identity.student_id_number,
                access_policy="restricted"
            )
            db.add(identity)

        # Handle Suspect Details
        if complaint_in.suspect_details:
            for s in complaint_in.suspect_details:
                suspect = SuspectDetail(
                    complaint_id=complaint.id,
                    name=s.name,
                    department=s.department,
                    phone=s.phone,
                    other_description=s.other_description,
                    details_visibility="authority_only"
                )
                db.add(suspect)

        db.flush()
        db.refresh(complaint)

        # Initial Status History
        history = CaseStatusHistory(
            complaint_id=complaint.id,
            previous_status="none",
            new_status="submitted",
            reason="Report submitted successfully"
        )
        db.add(history)

        # Urgent Fast-Track
        if complaint_in.is_urgent:
            EscalationService.escalate_single_complaint(
                db=db,
                complaint=complaint,
                target_level=1,
                reason="Immediate safety alert flagged by reporter during submission"
            )

        # Scan for Candidate Matches (Section 23)
        MatchingService.check_and_flag_candidates(db, complaint)

        # Audit Log
        AuditService.log_event(
            db=db,
            action="COMPLAINT_SUBMITTED",
            resource_type="complaint",
            resource_id=complaint.public_reference,
            reason=f"Mode: {complaint.reporting_mode}, Urgent: {complaint.is_urgent}",
            ip_address=client_ip
        )

        db.commit()
        db.refresh(complaint)
        return complaint, raw_tracking_secret
