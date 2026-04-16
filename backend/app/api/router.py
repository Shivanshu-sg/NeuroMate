from fastapi import APIRouter

from app.api.routes import chunks, health, kb, query, reports

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(query.router, tags=["query"])
api_router.include_router(kb.router, tags=["kb"])
api_router.include_router(chunks.router, tags=["chunks"])
