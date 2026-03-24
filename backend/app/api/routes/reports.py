from fastapi import APIRouter, File, UploadFile

from app.schemas.report import ReportUploadResponse
from app.services.report_service import report_service

router = APIRouter()


@router.post("/upload", response_model=ReportUploadResponse)
async def upload_report(file: UploadFile = File(...)) -> ReportUploadResponse:
    file_bytes = await file.read()
    return report_service.process_upload(file.filename, file_bytes)
