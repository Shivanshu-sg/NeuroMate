import json

from app.models.chunk import Chunk
from app.rag.vector_store import KnowledgeBaseVectorStore, PatientVectorStore


class ChunkIndexer:
    def __init__(self) -> None:
        self.patient_vector_store = PatientVectorStore()
        self.kb_vector_store = KnowledgeBaseVectorStore()

    def index_chunks(self, chunks: list[Chunk]) -> int:
        if not chunks:
            return 0

        patient_chunks = [chunk for chunk in chunks if not chunk.source_type.startswith("kb")]
        kb_chunks = [chunk for chunk in chunks if chunk.source_type.startswith("kb")]

        if patient_chunks:
            self._index_to_store(self.patient_vector_store.store, patient_chunks)
        if kb_chunks:
            self._index_to_store(self.kb_vector_store.store, kb_chunks)

        return len(patient_chunks) + len(kb_chunks)

    def _index_to_store(self, store, chunks: list[Chunk]) -> None:
        ids = [chunk.chunk_id for chunk in chunks]
        texts = [chunk.text for chunk in chunks]
        metadatas = [self._build_metadata(chunk) for chunk in chunks]
        store.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    def _build_metadata(self, chunk: Chunk) -> dict:
        parsed_metadata = {}
        if chunk.metadata_json:
            try:
                raw = json.loads(chunk.metadata_json)
                if isinstance(raw, dict):
                    parsed_metadata = raw
            except json.JSONDecodeError:
                parsed_metadata = {"metadata_parse_error": "invalid_json"}

        metadata = {
            "chunk_id": chunk.chunk_id,
            "report_id": chunk.report_id or "",
            "source_type": chunk.source_type,
            "source_url": chunk.source_url or "",
        }
        metadata.update({str(k): self._as_scalar(v) for k, v in parsed_metadata.items()})
        return metadata

    def _as_scalar(self, value):
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)
