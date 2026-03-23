from fastapi import APIRouter

from app.schemas.report import ReportUploadResponse
from app.services.report_service import report_service

router = APIRouter()


@router.post("/upload", response_model=ReportUploadResponse)
async def upload_report() -> ReportUploadResponse:
    return report_service.create_placeholder_response()
