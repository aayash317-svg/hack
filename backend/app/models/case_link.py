from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base


class CaseLink(Base):
    __tablename__ = "case_links"
    __table_args__ = (
        UniqueConstraint("complaint_id", "related_complaint_id", name="uq_case_links_pair"),
        CheckConstraint("complaint_id != related_complaint_id", name="ck_case_links_not_self"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    related_complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    review_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False
    )  # pending, confirmed, rejected, needs_more_review
    reviewed_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
