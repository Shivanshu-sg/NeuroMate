from app.db.session import SessionLocal
from app.models.chunk import Chunk


class ChunkRepository:
    def save_many(self, chunks: list[Chunk]) -> list[Chunk]:
        if not chunks:
            return []

        with SessionLocal() as session:
            session.add_all(chunks)
            session.commit()
            for chunk in chunks:
                session.refresh(chunk)
                session.expunge(chunk)
            return chunks

    def get_by_report(self, report_id: str) -> list[Chunk]:
        with SessionLocal() as session:
            rows = session.query(Chunk).filter(Chunk.report_id == report_id).all()
            for row in rows:
                session.expunge(row)
            return rows

    def get_by_ids(self, chunk_ids: list[str]) -> list[Chunk]:
        if not chunk_ids:
            return []
        with SessionLocal() as session:
            rows = session.query(Chunk).filter(Chunk.chunk_id.in_(chunk_ids)).all()
            for row in rows:
                session.expunge(row)
            return rows

    def get_by_id(self, chunk_id: str) -> Chunk | None:
        with SessionLocal() as session:
            row = session.get(Chunk, chunk_id)
            if row is None:
                return None
            session.expunge(row)
            return row
        
    def get_by_texts(self, texts: list[str]) -> list[Chunk]:
        if not texts:
            return []
        with SessionLocal() as session:
            rows = session.query(Chunk).filter(Chunk.text.in_(texts)).all()
            for row in rows:
                session.expunge(row)
            return rows
        
    def get_by_source_url(self, source_url: str) -> list[Chunk]:
        with SessionLocal() as session:
            rows = session.query(Chunk).filter(Chunk.source_url == source_url).all()
            for row in rows:
                session.expunge(row)
            return rows


chunk_repository = ChunkRepository()
