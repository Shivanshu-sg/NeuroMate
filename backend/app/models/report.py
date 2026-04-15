import json
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ReportRecord(Base):
    __tablename__ = "reports"

    report_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.user_id"), nullable=True, index=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, default="", nullable=False)
    extraction_status: Mapped[str] = mapped_column(default="pending", nullable=False)
    citations_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    extracted_data_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = relationship("User", back_populates="reports")
    chunks = relationship("Chunk", back_populates="report", cascade="all, delete-orphan")
    queries = relationship("Query", back_populates="report", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_reports_user_created_at", "user_id", "created_at"),
    )

    @property
    def extracted_data(self) -> dict:
        return json.loads(self.extracted_data_json)

    @extracted_data.setter
    def extracted_data(self, value: dict) -> None:
        self.extracted_data_json = json.dumps(value)
