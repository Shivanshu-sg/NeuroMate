from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import query_service

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_report(payload: QueryRequest) -> QueryResponse:
    return query_service.answer_query(
        query_text=payload.query_text,
        report_id=payload.report_id,
        top_k=payload.top_k,
    )
