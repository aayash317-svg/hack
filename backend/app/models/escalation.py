from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base


class Escalation(Base):
    __tablename__ = "escalations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    case_group_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("case_groups.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    complaint_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("complaints.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 = HOD, 2 = Dean, 3 = Higher Authority
    authority_user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False
    )  # pending, notified, acknowledged, completed, cancelled
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
