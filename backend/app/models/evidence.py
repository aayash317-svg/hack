from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    complaint_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("complaints.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    storage_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    original_filename_display: Mapped[str] = mapped_column(String(255), nullable=False)
    verified_media_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    complaint: Mapped["Complaint"] = relationship("Complaint", back_populates="evidence_items")
