import json
from uuid import uuid4

from fastapi import HTTPException, status

from app.db.repositories.chunk_repository import chunk_repository
from app.db.repositories.report_repository import report_repository
from app.core.config import settings
from app.extractors.pdf_extractor import PDFExtractor
from app.extractors.genetic_report_extractor import GeneticReportExtractor
from app.models.report import ReportRecord
from app.rag.chunk_indexer import ChunkIndexer
from app.rag.document_builder import PatientDocumentBuilder
from app.schemas.report import ReportUploadResponse

from datetime import datetime


class ReportService:
    def __init__(self) -> None:
        self.pdf_extractor = PDFExtractor()
        self.genetic_report_extractor = GeneticReportExtractor()
        self.document_builder = PatientDocumentBuilder()
        self.chunk_indexer: ChunkIndexer | None = None

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

        time_now = datetime.now()
        raw_text, _stored_path = self.pdf_extractor.extract_text(file_bytes, filename)

        if report_repository.get_report(raw_text) is not None:
            report = report_repository.get_report(raw_text)
            return ReportUploadResponse(
                status="completed",
                message="Report with identical content already exists. Skipping extraction and indexing.",
                report_id=report.report_id,
                filename=filename,
                raw_text=raw_text,
                extracted_data=json.loads(report.extracted_data_json) if report.extracted_data_json else None,
            )
        
        
        print("time taken for pdf to text extraction", datetime.now() - time_now)

        if not raw_text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No extractable text was found in the PDF.",
            )

        time_now = datetime.now()
        try:
            extracted_data = self.genetic_report_extractor.extract(raw_text)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Genetic report extraction failed: {exc}",
            ) from exc
        print("time taken for genetic report extraction", datetime.now() - time_now)

        report = ReportRecord(
            report_id=str(uuid4()),
            user_id=settings.default_local_user_id,
            filename=filename,
            raw_text=raw_text,
            extraction_status="completed",
            extracted_data_json=json.dumps(extracted_data),
        )

        report_repository.save(report)
        patient_chunks = self.document_builder.build_patient_chunks(
            report_id=report.report_id,
            raw_text=raw_text,
            extracted_data=extracted_data,
        )
        chunk_repository.save_many(patient_chunks)
        indexed_count = 0
        indexing_warning = ""
        try:
            if self.chunk_indexer is None:
                self.chunk_indexer = ChunkIndexer()
            indexed_count = self.chunk_indexer.index_chunks(patient_chunks)
        except Exception as exc:
            indexing_warning = f" Vector indexing skipped ({exc.__class__.__name__})."

        return ReportUploadResponse(
            status="completed",
            message=(
                f"PDF extracted, genetic information parsed, and report stored with {len(patient_chunks)} chunks. "
                f"Indexed {indexed_count} chunks in vector DB.{indexing_warning}"
            ),
            report_id=report.report_id,
            filename=report.filename,
            raw_text=report.raw_text,
            extracted_data=extracted_data,
        )


report_service = ReportService()
