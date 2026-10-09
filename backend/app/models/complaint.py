from datetime import datetime, date, timezone
from typing import Optional, List
from sqlalchemy import Integer, String, Boolean, Date, DateTime, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    public_reference: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    tracking_secret_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    reporting_mode: Mapped[str] = mapped_column(String(20), nullable=False)  # confidential, anonymous
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # offline, online
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    incident_date: Mapped[date] = mapped_column(Date, nullable=False)
    incident_time: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    location_or_platform: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_urgent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default="submitted",
        nullable=False
    )  # submitted, under_review, pending_match_review, escalated, awaiting_information, resolved, closed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    reporter_identity: Mapped[Optional["ReporterIdentity"]] = relationship(
        "ReporterIdentity",
        back_populates="complaint",
        uselist=False,
        cascade="all, delete-orphan"
    )
    suspect_details: Mapped[List["SuspectDetail"]] = relationship(
        "SuspectDetail",
        back_populates="complaint",
        cascade="all, delete-orphan"
    )
    evidence_items: Mapped[List["Evidence"]] = relationship(
        "Evidence",
        back_populates="complaint",
        cascade="all, delete-orphan"
    )
    status_history: Mapped[List["CaseStatusHistory"]] = relationship(
        "CaseStatusHistory",
        back_populates="complaint",
        order_by="CaseStatusHistory.created_at.desc()",
        cascade="all, delete-orphan"
    )
