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


settings = Settings()
