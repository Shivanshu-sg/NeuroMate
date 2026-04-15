from fastapi import APIRouter, File, UploadFile

from app.schemas.report import ReportUploadResponse
from app.services.report_service import report_service

from datetime import datetime

router = APIRouter()


@router.post("/upload", response_model=ReportUploadResponse)
async def upload_report(file: UploadFile = File(...)) -> ReportUploadResponse:
    timenow = datetime.now()
    file_bytes = await file.read()
    result = report_service.process_upload(file.filename, file_bytes)
    print("Total time taken for report processing", datetime.now() - timenow)
    return result
