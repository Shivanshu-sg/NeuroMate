from pydantic import BaseModel


class ReportUploadResponse(BaseModel):
    status: str
    message: str

