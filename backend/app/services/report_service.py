import json
from uuid import uuid4

from fastapi import HTTPException, status

from app.db.repositories.report_repository import report_repository
from app.extractors.pdf_extractor import PDFExtractor
from app.extractors.genetic_report_extractor import GeneticReportExtractor
from app.models.report import ReportRecord
from app.schemas.report import ReportUploadResponse


class ReportService:
    def __init__(self) -> None:
        self.pdf_extractor = PDFExtractor()
        self.genetic_report_extractor = GeneticReportExtractor()

    def process_upload(self, filename: str | None, file_bytes: bytes) -> ReportUploadResponse:
        if not filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must have a filename.",
            )

        if not filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF uploads are supported.",
            )

        raw_text, _stored_path = self.pdf_extractor.extract_text(file_bytes, filename)

        if not raw_text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No extractable text was found in the PDF.",
            )

        try:
            extracted_data = self.genetic_report_extractor.extract(raw_text)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Genetic report extraction failed: {exc}",
            ) from exc
        

        report = ReportRecord(
            report_id=str(uuid4()),
            filename=filename,
            raw_text=raw_text,
            extraction_status="completed",
            citations_json="[]",
            extracted_data_json=json.dumps(extracted_data),
        )

        report_repository.save(report)

        return ReportUploadResponse(
            status="completed",
            message="PDF extracted, genetic information parsed, and report stored successfully.",
            report_id=report.report_id,
            filename=report.filename,
            raw_text=report.raw_text,
            extracted_data=extracted_data,
        )


report_service = ReportService()
