from fastapi import APIRouter

from app.schemas.kb import KBIndexResponse
from app.services.kb_service import kb_service

router = APIRouter()


@router.post("/kb/index", response_model=KBIndexResponse)
async def index_kb() -> KBIndexResponse:
    return kb_service.index_local_kb()
