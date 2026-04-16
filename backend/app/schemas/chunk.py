from pydantic import BaseModel


class ChunkDetailResponse(BaseModel):
    chunk_id: str
    report_id: str | None
    source_type: str
    source_url: str | None
    text: str
    metadata_json: str
