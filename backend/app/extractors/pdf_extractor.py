from pathlib import Path
from uuid import uuid4

from langchain_community.document_loaders import PyPDFLoader

from app.core.config import settings
from app.utils.text import normalize_whitespace


class PDFExtractor:
    """Extract text from PDFs using LangChain document loaders."""

    def extract_text(self, file_bytes: bytes, filename: str) -> tuple[str, Path]:
        settings.uploads_dir.mkdir(parents=True, exist_ok=True)
        safe_name = Path(filename).name or f"{uuid4()}.pdf"
        stored_path = settings.uploads_dir / f"{uuid4()}_{safe_name}"
        stored_path.write_bytes(file_bytes)

        loader = PyPDFLoader(str(stored_path))
        documents = loader.load()
        text = "\n".join(document.page_content for document in documents if document.page_content).strip()

        return normalize_whitespace(text), stored_path
