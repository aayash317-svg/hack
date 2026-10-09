from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.models.audit_log import AuditLog
from backend.app.models.notification import Notification
from backend.app.schemas.auth import UserResponse, UserCreate
from backend.app.core.security import get_password_hash
from backend.app.core.permissions import require_roles, get_current_user
from backend.app.core.config import settings

router = APIRouter(prefix="", tags=["Administration"])


@router.get("/admin/users", response_model=List[UserResponse])
def list_admin_users(
    current_user: User = Depends(require_roles(["administrator"])),
    db: Session = Depends(get_db)
):
    """Lists all user accounts (Admin only)."""
    return db.query(User).all()


@router.post("/admin/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_admin_user(
    user_in: UserCreate,
    current_user: User = Depends(require_roles(["administrator"])),
    db: Session = Depends(get_db)
):
    """Creates an authorized authority user account (Admin only)."""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
        department=user_in.department,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.patch("/admin/users/{user_id}/toggle", response_model=UserResponse)
def toggle_user_active(
    user_id: int,
    current_user: User = Depends(require_roles(["administrator"])),
    db: Session = Depends(get_db)
):
    """Enables or disables an authority account."""
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    target_user.is_active = not target_user.is_active
    db.commit()
    db.refresh(target_user)
    return target_user


@router.get("/admin/audit-logs")
def list_audit_logs(
    action: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    current_user: User = Depends(require_roles(["administrator"])),
    db: Session = Depends(get_db)
):
    """Returns immutable security audit trail events."""
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()

    return [
        {
            "id": l.id,
            "actor_user_id": l.actor_user_id,
            "action": l.action,
            "resource_type": l.resource_type,
            "resource_id": l.resource_id,
            "reason": l.reason,
            "ip_address": l.ip_address,
            "timestamp": l.timestamp
        }
        for l in logs
    ]


@router.get("/admin/configuration")
def get_system_configuration(
    current_user: User = Depends(require_roles(["administrator", "hod", "dean", "higher_authority"]))
):
    """Returns non-secret institution parameters."""
    return {
        "institution_name": settings.INSTITUTION_NAME,
        "emergency_helpline": settings.EMERGENCY_HELPLINE,
        "security_gate_contact": settings.SECURITY_GATE_CONTACT,
        "max_upload_size_bytes": settings.MAX_UPLOAD_SIZE_BYTES,
        "allowed_media_types": settings.ALLOWED_MEDIA_TYPES,
        "version": settings.VERSION
    }


@router.get("/authority/notifications")
def get_user_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves in-app notifications for the signed-in authority user."""
    notifs = db.query(Notification).filter(
        Notification.recipient_user_id == current_user.id
    ).order_by(Notification.created_at.desc()).limit(20).all()

    return [
        {
            "id": n.id,
            "case_reference": n.case_reference,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifs
    ]


@router.patch("/authority/notifications/{notif_id}/read")
def mark_notification_read(
    notif_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marks a notification as read."""
    notif = db.query(Notification).filter(
        Notification.id == notif_id,
        Notification.recipient_user_id == current_user.id
    ).first()
    if notif:
        notif.is_read = True
        db.commit()
    return {"message": "Notification marked as read."}
