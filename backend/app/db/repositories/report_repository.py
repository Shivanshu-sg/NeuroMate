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

    def get_latest_for_user(self, user_id: str) -> ReportRecord | None:
        with SessionLocal() as session:
            report = (
                session.query(ReportRecord)
                .filter(ReportRecord.user_id == user_id)
                .order_by(ReportRecord.created_at.desc())
                .first()
            )
            if report is None:
                return None
            session.expunge(report)
            return report
        
    def get_report(self, report_text: str) -> ReportRecord | None:
        with SessionLocal() as session:
            report = session.query(ReportRecord).filter(ReportRecord.raw_text == report_text).first()
            if report is None:
                return None
            session.expunge(report)
            return report
        

report_repository = SQLiteReportRepository()
