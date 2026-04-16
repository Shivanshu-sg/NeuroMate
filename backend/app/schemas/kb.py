from pydantic import BaseModel


class KBIndexResponse(BaseModel):
    status: str
    message: str
    indexed_chunks: int
