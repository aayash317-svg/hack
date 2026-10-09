from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    name: str
    email: str
    role: str
    department: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department: Optional[str] = None
    is_active: bool


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # student, hod, dean, higher_authority, administrator
    department: Optional[str] = None
