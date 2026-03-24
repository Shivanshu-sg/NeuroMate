from pydantic import BaseModel


class ReportUploadResponse(BaseModel):
    status: str
    message: str
    report_id: str
    filename: str
    raw_text: str
