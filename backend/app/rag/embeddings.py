from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings


class EmbeddingService:
    _cached_embeddings = None

    def __init__(self) -> None:
        if EmbeddingService._cached_embeddings is None:
            EmbeddingService._cached_embeddings = HuggingFaceEmbeddings(
                model_name=settings.embedding_model_name,
                model_kwargs={"local_files_only": True},
            )
        self._embeddings = EmbeddingService._cached_embeddings

    @property
    def embeddings(self) -> HuggingFaceEmbeddings:
        return self._embeddings
