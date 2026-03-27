from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.report import ReportRecord


class SQLiteReportRepository:
    def save(self, report: ReportRecord) -> ReportRecord:
        with SessionLocal() as session:
            persisted = session.merge(report)
            session.commit()
            session.refresh(persisted)
            session.expunge(persisted)
            return persisted

    def get(self, report_id: str) -> ReportRecord | None:
        with SessionLocal() as session:
            report = session.get(ReportRecord, report_id)
            if report is None:
                return None
            session.expunge(report)
            return report

report_repository = SQLiteReportRepository()
