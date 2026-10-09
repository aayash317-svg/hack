from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SuspectDetailResponse(BaseModel):
    id: int
    name: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    other_description: Optional[str] = None


class EvidenceResponse(BaseModel):
    id: int
    original_filename_display: str
    verified_media_type: str
    file_size: int
    uploaded_at: datetime


class StatusHistoryResponse(BaseModel):
    id: int
    previous_status: str
    new_status: str
    changed_by_name: Optional[str] = None
    reason: Optional[str] = None
    created_at: datetime


class UnmaskedIdentityResponse(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    student_id_number: Optional[str] = None
    access_policy: str


class CaseListItem(BaseModel):
    id: int
    public_reference: str
    reporting_mode: str
    type: str
    category: str
    incident_date: date
    location_or_platform: str
    is_urgent: bool
    status: str
    created_at: datetime
    case_group_id: Optional[int] = None
    group_reference: Optional[str] = None
    confirmed_reports_in_group: int = 1


class CaseDetailResponse(BaseModel):
    id: int
    public_reference: str
    reporting_mode: str
    type: str
    category: str
    incident_date: date
    incident_time: Optional[str] = None
    location_or_platform: str
    description: str
    is_urgent: bool
    status: str
    created_at: datetime
    updated_at: datetime
    suspect_details: List[SuspectDetailResponse] = []
    evidence_items: List[EvidenceResponse] = []
    status_history: List[StatusHistoryResponse] = []
    case_group_id: Optional[int] = None
    group_reference: Optional[str] = None
    confirmed_reports_in_group: int = 1
    current_escalation_level: int = 1
    has_confidential_identity: bool = False
    unmasked_identity: Optional[UnmaskedIdentityResponse] = None


class StatusUpdateRequest(BaseModel):
    new_status: str = Field(..., pattern="^(submitted|under_review|pending_match_review|escalated|awaiting_information|resolved|closed)$")
    reason: str = Field(..., min_length=3)


class EscalateRequest(BaseModel):
    target_level: int = Field(..., ge=1, le=3)
    reason: str = Field(..., min_length=3)


class RequestIdentityAccess(BaseModel):
    justified_reason: str = Field(..., min_length=10)
