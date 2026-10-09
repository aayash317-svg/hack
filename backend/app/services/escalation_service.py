from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from backend.app.models.escalation import Escalation
from backend.app.models.case_group import CaseGroup, CaseGroupMember
from backend.app.models.complaint import Complaint
from backend.app.models.status_history import CaseStatusHistory
from backend.app.models.notification import Notification
from backend.app.models.user import User
from backend.app.models.audit_log import AuditLog


class EscalationService:
    @classmethod
    def evaluate_group_escalation(
        cls,
        db: Session,
        case_group_id: int,
        reason: Optional[str] = None
    ) -> Optional[Escalation]:
        """
        Calculates and applies Section 23 repeat-report escalation level for a case group.
        1 confirmed report -> Level 1 (HOD)
        2 distinct confirmed reports -> Level 2 (Dean)
        3+ distinct confirmed reports -> Level 3 (Higher Authority)
        """
        # Count distinct confirmed complaints in this case group
        distinct_count = db.query(func.count(distinct(CaseGroupMember.complaint_id))).filter(
            CaseGroupMember.case_group_id == case_group_id
        ).scalar() or 0

        if distinct_count == 0:
            return None

        # Determine target level per Section 23
        if distinct_count == 1:
            target_level = 1
            target_role = "hod"
            tier_name = "HOD (Level 1)"
        elif distinct_count == 2:
            target_level = 2
            target_role = "dean"
            tier_name = "Dean (Level 2)"
        else:
            target_level = 3
            target_role = "higher_authority"
            tier_name = "Higher Authority (Level 3)"

        # Check if already escalated to this level or higher
        existing = db.query(Escalation).filter(
            Escalation.case_group_id == case_group_id,
            Escalation.level >= target_level
        ).first()

        if existing:
            return None  # Do not duplicate escalation

        # Find assigned authority user
        authority = db.query(User).filter(User.role == target_role, User.is_active == True).first()
        authority_id = authority.id if authority else None

        escalation_reason = reason or (
            f"Automated Section 23 pattern escalation: Group contains {distinct_count} distinct confirmed "
            f"related incident reports. Escalated to {tier_name}."
        )

        escalation = Escalation(
            case_group_id=case_group_id,
            level=target_level,
            authority_user_id=authority_id,
            reason=escalation_reason,
            status="pending"
        )
        db.add(escalation)

        # Update complaints in group and create status histories
        members = db.query(CaseGroupMember).filter(CaseGroupMember.case_group_id == case_group_id).all()
        for member in members:
            c = db.query(Complaint).filter(Complaint.id == member.complaint_id).first()
            if c:
                prev_status = c.status
                if target_level > 1 and prev_status != "closed":
                    c.status = "escalated"
                    history = CaseStatusHistory(
                        complaint_id=c.id,
                        previous_status=prev_status,
                        new_status="escalated",
                        changed_by=authority_id,
                        reason=escalation_reason
                    )
                    db.add(history)

                # Send notification
                if authority_id:
                    notif = Notification(
                        recipient_user_id=authority_id,
                        case_reference=c.public_reference,
                        title=f"Case Group Escalated to {tier_name}",
                        message=f"Case {c.public_reference} has escalated to {tier_name} due to confirmed pattern."
                    )
                    db.add(notif)

        # Log audit
        audit = AuditLog(
            action="GROUP_ESCALATED",
            resource_type="case_group",
            resource_id=str(case_group_id),
            reason=escalation_reason
        )
        db.add(audit)
        db.flush()
        return escalation

    @classmethod
    def escalate_single_complaint(
        cls,
        db: Session,
        complaint: Complaint,
        target_level: int,
        reason: str,
        actor_id: Optional[int] = None
    ) -> Escalation:
        """Manually or urgently escalates an individual complaint."""
        role_map = {1: "hod", 2: "dean", 3: "higher_authority"}
        target_role = role_map.get(target_level, "higher_authority")
        authority = db.query(User).filter(User.role == target_role, User.is_active == True).first()
        authority_id = authority.id if authority else None

        escalation = Escalation(
            complaint_id=complaint.id,
            level=target_level,
            authority_user_id=authority_id,
            reason=reason,
            status="pending"
        )
        db.add(escalation)

        prev_status = complaint.status
        complaint.status = "escalated"

        history = CaseStatusHistory(
            complaint_id=complaint.id,
            previous_status=prev_status,
            new_status="escalated",
            changed_by=actor_id,
            reason=reason
        )
        db.add(history)

        if authority_id:
            notif = Notification(
                recipient_user_id=authority_id,
                case_reference=complaint.public_reference,
                title=f"Urgent Case Escalated to Level {target_level}",
                message=f"Case {complaint.public_reference} was escalated: {reason}"
            )
            db.add(notif)

        audit = AuditLog(
            actor_user_id=actor_id,
            action="CASE_ESCALATED",
            resource_type="complaint",
            resource_id=str(complaint.id),
            reason=reason
        )
        db.add(audit)
        db.flush()
        return escalation
