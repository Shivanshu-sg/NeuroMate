from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Query(Base):
    __tablename__ = "queries"

    query_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.user_id"), nullable=True, index=True)
    report_id: Mapped[str] = mapped_column(ForeignKey("reports.report_id"), nullable=False, index=True)
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="queries")
    report = relationship("ReportRecord", back_populates="queries")
    citations = relationship("QueryCitation", back_populates="query", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_queries_user_report_created_at", "user_id", "report_id", "created_at"),
    )
