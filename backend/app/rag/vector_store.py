from langchain_community.vectorstores import Chroma

from app.core.config import settings
from app.rag.embeddings import EmbeddingService


class BaseVectorStore:
    def __init__(self, collection_name: str) -> None:
        settings.vector_db_path.mkdir(parents=True, exist_ok=True)
        embedding_service = EmbeddingService()
        self._store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_service.embeddings,
            persist_directory=str(settings.vector_db_path),
        )

    @property
    def store(self) -> Chroma:
        return self._store


class PatientVectorStore(BaseVectorStore):
    def __init__(self) -> None:
        super().__init__(collection_name=settings.patient_chunk_collection_name)


class KnowledgeBaseVectorStore(BaseVectorStore):
    def __init__(self) -> None:
        super().__init__(collection_name=settings.kb_chunk_collection_name)
