from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.api.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


def run_startup_migrations() -> None:
    inspector = inspect(engine)
    if "reports" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("reports")}
    if "extracted_data_json" not in existing_columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE reports ADD COLUMN extracted_data_json TEXT NOT NULL DEFAULT '{}'")
            )


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    run_startup_migrations()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_app()
