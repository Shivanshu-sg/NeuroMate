from uuid import uuid4

from app.db.repositories.report_repository import report_repository
from app.models.report import ReportRecord
from app.schemas.report import ReportUploadResponse


class ReportService:
    def create_placeholder_response(self) -> ReportUploadResponse:
        report = ReportRecord(
            report_id=str(uuid4()),
            filename="placeholder.txt",
            extraction_status="pending",
        )
        report_repository.save(report)
        return ReportUploadResponse(
            status="pending",
            message=f"Report processing service is ready for extraction integration. Placeholder report saved with id {report.report_id}.",
        )


report_service = ReportService()
