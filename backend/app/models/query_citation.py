from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class QueryCitation(Base):
    __tablename__ = "query_citations"

    query_citation_id: Mapped[str] = mapped_column(primary_key=True)
    query_id: Mapped[str] = mapped_column(ForeignKey("queries.query_id"), nullable=False, index=True)
    chunk_id: Mapped[str] = mapped_column(ForeignKey("chunks.chunk_id"), nullable=False, index=True)
    rank: Mapped[int] = mapped_column(nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    query = relationship("Query", back_populates="citations")
    chunk = relationship("Chunk", back_populates="query_citations")

    __table_args__ = (
        Index("ix_query_citations_query_rank", "query_id", "rank"),
    )
