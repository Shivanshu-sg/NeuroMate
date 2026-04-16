from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "NeuroMate Backend"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    base_dir: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data")
    uploads_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data" / "uploads")
    database_path: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data" / "neuromate.db")
    vector_db_path: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "chroma_db")
    patient_chunk_collection_name: str = "patient_chunks"
    kb_chunk_collection_name: str = "kb_chunks"
    kb_sources_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "kb")
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    default_local_user_id: str = "local_default_user"


settings = Settings()
