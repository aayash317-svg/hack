from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models.audit_log import AuditLog


class AuditService:
    @staticmethod
    def log_event(
        db: Session,
        action: str,
        resource_type: str,
        resource_id: str,
        actor_user_id: Optional[int] = None,
        reason: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        """Records an immutable security audit event."""
        log = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id),
            reason=reason,
            ip_address=ip_address
        )
        db.add(log)
        db.flush()
        return log
