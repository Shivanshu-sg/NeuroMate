from app.rag.vector_store import KnowledgeBaseVectorStore, PatientVectorStore


class Retriever:
    def __init__(self) -> None:
        self.patient_vector_store: PatientVectorStore | None = None
        self.kb_vector_store: KnowledgeBaseVectorStore | None = None

    def _patient_store(self) -> PatientVectorStore:
        if self.patient_vector_store is None:
            self.patient_vector_store = PatientVectorStore()
        return self.patient_vector_store

    def _kb_store(self) -> KnowledgeBaseVectorStore:
        if self.kb_vector_store is None:
            self.kb_vector_store = KnowledgeBaseVectorStore()
        return self.kb_vector_store

    def retrieve_patient_chunks(self, query_text: str, report_id: str, top_k: int = 5) -> list[dict]:
        results = self._patient_store().store.similarity_search_with_score(
            query_text,
            k=top_k,
            filter={"report_id": report_id},
        )

        retrieved: list[dict] = []
        for document, score in results:
            metadata = document.metadata or {}
            chunk_id = str(metadata.get("chunk_id", "")).strip()
            if not chunk_id:
                continue
            retrieved.append(
                {
                    "chunk_id": chunk_id,
                    "score": float(score),
                    "text": document.page_content,
                    "metadata": metadata,
                }
            )
        return retrieved

    def retrieve_kb_chunks(self, query_text: str, top_k: int = 3) -> list[dict]:
        results = self._kb_store().store.similarity_search_with_score(
            query_text,
            k=top_k,
        )

        retrieved: list[dict] = []
        for document, score in results:
            metadata = document.metadata or {}
            chunk_id = str(metadata.get("chunk_id", "")).strip()
            if not chunk_id:
                continue
            retrieved.append(
                {
                    "chunk_id": chunk_id,
                    "score": float(score),
                    "text": document.page_content,
                    "metadata": metadata,
                }
            )
        return retrieved
