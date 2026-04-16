from pydantic import BaseModel


class QueryRequest(BaseModel):
    query_text: str
    report_id: str | None = None
    top_k: int = 5


class QueryCitationResponse(BaseModel):
    chunk_id: str
    rank: int
    score: float
    source_type: str
    source_url: str | None
    excerpt: str


class QueryResponse(BaseModel):
    query_id: str
    report_id: str
    answer: str
    citations: list[QueryCitationResponse]
