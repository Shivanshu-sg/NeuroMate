from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Chunk(Base):
    __tablename__ = "chunks"

    chunk_id: Mapped[str] = mapped_column(primary_key=True)
    report_id: Mapped[str | None] = mapped_column(ForeignKey("reports.report_id"), nullable=True, index=True)
    source_type: Mapped[str] = mapped_column(nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str | None] = mapped_column(nullable=True)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    report = relationship("ReportRecord", back_populates="chunks")
    query_citations = relationship("QueryCitation", back_populates="chunk", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_chunks_report_source_type", "report_id", "source_type"),
    )
