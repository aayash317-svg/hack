from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from backend.app.models.user import User
from backend.app.core.security import verify_password, create_access_token
from backend.app.core.permissions import get_current_user
from backend.app.services.audit_service import AuditService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_db)
):
    """Signs in an authorized user and sets an HttpOnly session cookie."""
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        AuditService.log_event(
            db=db,
            action="LOGIN_FAILED",
            resource_type="auth",
            resource_id=login_data.email,
            reason="Invalid credentials",
            ip_address=request.client.host if request.client else None
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled. Contact system administrator."
        )

    token = create_access_token(data={"sub": str(user.id), "role": user.role, "name": user.name})

    # Set secure HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # Set to True in production HTTPS
        max_age=60 * 60 * 24
    )

    AuditService.log_event(
        db=db,
        action="LOGIN_SUCCESS",
        resource_type="user",
        resource_id=str(user.id),
        actor_user_id=user.id,
        reason=f"Role: {user.role}",
        ip_address=request.client.host if request.client else None
    )
    db.commit()

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        department=user.department
    )


@router.post("/logout")
def logout(response: Response):
    """Clears the session cookie."""
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully."}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Returns current signed-in user information."""
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        department=current_user.department,
        is_active=current_user.is_active
    )
