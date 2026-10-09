from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base


class ReporterIdentity(Base):
    __tablename__ = "reporter_identities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    student_id_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    access_policy: Mapped[str] = mapped_column(String(50), default="restricted", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    complaint: Mapped["Complaint"] = relationship("Complaint", back_populates="reporter_identity")
