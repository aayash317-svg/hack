from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MatchReviewCandidate(BaseModel):
    id: int
    public_reference: str
    type: str
    category: str
    incident_date: date
    location_or_platform: str
    description: str
    suspect_summary: Optional[str] = None


class MatchReviewItem(BaseModel):
    link_id: int
    complaint_a: MatchReviewCandidate
    complaint_b: MatchReviewCandidate
    matched_features: List[str]
    created_at: datetime


class MatchDecisionRequest(BaseModel):
    decision: str = Field(..., pattern="^(confirm|reject|needs_more_review)$")
    reason: str = Field(..., min_length=3)
