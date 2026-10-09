from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class ReporterIdentityCreate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    student_id_number: Optional[str] = Field(None, max_length=100)


class SuspectDetailCreate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    department: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    other_description: Optional[str] = None


class ComplaintCreate(BaseModel):
    reporting_mode: str = Field(..., pattern="^(confidential|anonymous)$")
    type: str = Field(..., pattern="^(offline|online)$")
    category: str = Field(..., min_length=2, max_length=100)
    incident_date: date
    incident_time: Optional[str] = Field(None, max_length=50)
    location_or_platform: str = Field(..., min_length=2, max_length=255)
    description: str = Field(..., min_length=10)
    is_urgent: bool = False
    reporter_identity: Optional[ReporterIdentityCreate] = None
    suspect_details: Optional[List[SuspectDetailCreate]] = None


class ComplaintSubmissionResponse(BaseModel):
    public_reference: str
    tracking_secret: str  # Note: displayed once upon submission!
    status: str
    reporting_mode: str
    is_urgent: bool
    created_at: datetime
    message: str
    urgent_guidance: Optional[str] = None
