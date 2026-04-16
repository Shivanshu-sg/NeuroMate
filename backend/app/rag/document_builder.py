import json
from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.chunk import Chunk


class PatientDocumentBuilder:
    def __init__(self) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=900,
            chunk_overlap=120,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def build_patient_chunks(self, report_id: str, raw_text: str, extracted_data: dict) -> list[Chunk]:
        chunks: list[Chunk] = []

        summary_text = self._build_summary_text(extracted_data)
        if summary_text:
            chunks.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    report_id=report_id,
                    source_type="patient_summary",
                    text=summary_text,
                    source_url=None,
                    metadata_json=json.dumps({"chunk_type": "summary", "source": "extracted_data_json"}),
                )
            )

        text_chunks = self._chunk_text(raw_text)
        for index, chunk_text in enumerate(text_chunks):
            chunks.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    report_id=report_id,
                    source_type="patient_report",
                    text=chunk_text,
                    source_url=None,
                    metadata_json=json.dumps(
                        {"chunk_type": "report_text", "chunk_index": index, "source": "raw_text"}
                    ),
                )
            )

        return chunks

    def _build_summary_text(self, extracted_data: dict) -> str:
        keys = [
            "patient_name",
            "age",
            "gender",
            "gene_name",
            "variant",
            "variant_type",
            "zygosity",
            "classification",
            "disease_name",
        ]
        parts: list[str] = []
        for key in keys:
            value = extracted_data.get(key)
            if value is None or value == "":
                continue
            parts.append(f"{key}: {value}")
        return "\n".join(parts).strip()

    def _chunk_text(self, text: str) -> list[str]:
        normalized = " ".join(text.split())
        if not normalized:
            return []
        return [chunk.strip() for chunk in self.text_splitter.split_text(normalized) if chunk.strip()]
