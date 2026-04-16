import json
from pathlib import Path
from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.db.repositories.chunk_repository import chunk_repository
from app.models.chunk import Chunk
from app.rag.chunk_indexer import ChunkIndexer
from app.schemas.kb import KBIndexResponse


class KBService:
    def __init__(self) -> None:
        self.chunk_indexer: ChunkIndexer | None = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def index_local_kb(self) -> KBIndexResponse:
        source_dir = settings.kb_sources_dir
        if not source_dir.exists():
            return KBIndexResponse(
                status="skipped",
                message=f"KB source directory not found at {source_dir}.",
                indexed_chunks=0,
            )

        chunks_to_save: list[Chunk] = []
        for file_path in source_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in {".txt", ".md"}:
                continue
            text = file_path.read_text(encoding="utf-8", errors="ignore").strip()
            if not text:
                continue
            if chunk_repository.get_by_source_url(str(file_path)):
                continue
            chunks_to_save.extend(self._build_chunks_from_text(file_path, text))


        # if chunk_repository.get_by_texts([chunk.text for chunk in chunks_to_save]):
        #     return KBIndexResponse(
        #         status="skipped",
        #         message="KB chunks with identical text already exist in the database. No new chunks indexed.",
        #         indexed_chunks=0,
        #     )

        saved_chunks = chunk_repository.save_many(chunks_to_save)
        if self.chunk_indexer is None:
            self.chunk_indexer = ChunkIndexer()
        indexed_count = self.chunk_indexer.index_chunks(saved_chunks)

        return KBIndexResponse(
            status="completed",
            message=f"Indexed {indexed_count} knowledge base chunks.",
            indexed_chunks=indexed_count,
        )

    def _build_chunks_from_text(self, file_path: Path, text: str) -> list[Chunk]:
        normalized = " ".join(text.split())
        if not normalized:
            return []
        built: list[Chunk] = []
        for index, part in enumerate(self.text_splitter.split_text(normalized)):
            part = part.strip()
            if part:
                built.append(
                    Chunk(
                        chunk_id=str(uuid4()),
                        report_id=None,
                        source_type="kb_doc",
                        text=part,
                        source_url=str(file_path),
                        metadata_json=json.dumps(
                            {
                                "chunk_type": "kb_text",
                                "file_name": file_path.name,
                                "file_path": str(file_path),
                                "chunk_index": index,
                            }
                        ),
                    )
                )

        return built


kb_service = KBService()
