from fastapi import APIRouter, HTTPException, status

from app.db.repositories.chunk_repository import chunk_repository
from app.schemas.chunk import ChunkDetailResponse

router = APIRouter()


@router.get("/chunks/{chunk_id}", response_model=ChunkDetailResponse)
async def get_chunk(chunk_id: str) -> ChunkDetailResponse:
    chunk = chunk_repository.get_by_id(chunk_id)
    if chunk is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk {chunk_id} not found.",
        )

    return ChunkDetailResponse(
        chunk_id=chunk.chunk_id,
        report_id=chunk.report_id,
        source_type=chunk.source_type,
        source_url=chunk.source_url,
        text=chunk.text,
        metadata_json=chunk.metadata_json,
    )
