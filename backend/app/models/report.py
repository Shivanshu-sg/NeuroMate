import json

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReportRecord(Base):
    __tablename__ = "reports"

    report_id: Mapped[str] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, default="", nullable=False)
    extraction_status: Mapped[str] = mapped_column(default="pending", nullable=False)
    citations_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)

    @property
    def citations(self) -> list[str]:
        return json.loads(self.citations_json)

    @citations.setter
    def citations(self, value: list[str]) -> None:
        self.citations_json = json.dumps(value)
