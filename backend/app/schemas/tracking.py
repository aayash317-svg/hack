from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel


class MilestoneItem(BaseModel):
    status: str
    label: str
    timestamp: datetime
    description: str


class TrackingResponse(BaseModel):
    public_reference: str
    reporting_mode: str
    status: str
    category: str
    type: str
    incident_date: date
    is_urgent: bool
    created_at: datetime
    timeline: List[MilestoneItem]
    public_message: str
