from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base


class CaseGroup(Base):
    __tablename__ = "case_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    group_reference: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)  # active, consolidated, archived
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    members: Mapped[list["CaseGroupMember"]] = relationship(
        "CaseGroupMember",
        back_populates="group",
        cascade="all, delete-orphan"
    )


class CaseGroupMember(Base):
    __tablename__ = "case_group_members"
    __table_args__ = (
        UniqueConstraint("case_group_id", "complaint_id", name="uq_case_group_member"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    case_group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("case_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    added_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    group: Mapped["CaseGroup"] = relationship("CaseGroup", back_populates="members")
