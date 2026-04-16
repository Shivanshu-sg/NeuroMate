from uuid import uuid4

from fastapi import HTTPException, status

from app.core.config import settings
from app.db.repositories.chunk_repository import chunk_repository
from app.db.repositories.query_repository import query_repository
from app.db.repositories.report_repository import report_repository
from app.models.query import Query
from app.models.query_citation import QueryCitation
from app.rag.generator import AnswerGenerator
from app.rag.retriever import Retriever
from app.schemas.query import QueryCitationResponse, QueryResponse


class QueryService:
    def __init__(self) -> None:
        self.retriever: Retriever | None = None
        self.generator: AnswerGenerator | None = None

    def answer_query(self, query_text: str, report_id: str | None, top_k: int = 5) -> QueryResponse:
        target_report_id = report_id or self._resolve_latest_report_id()
        report = report_repository.get(target_report_id)
        if report is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report {target_report_id} not found.",
            )

        retriever = self._retriever()
        generator = self._generator()

        bounded_k = max(1, min(top_k, 10))
        patient_k = max(1, int(round(bounded_k * 0.65)))
        kb_k = max(1, bounded_k - patient_k)

        patient_retrieved = retriever.retrieve_patient_chunks(
            query_text=query_text,
            report_id=target_report_id,
            top_k=patient_k,
        )
        kb_retrieved = retriever.retrieve_kb_chunks(
            query_text=query_text,
            top_k=kb_k,
        )

        retrieved = sorted(patient_retrieved + kb_retrieved, key=lambda item: item["score"])[:bounded_k]

        chunk_ids = [item["chunk_id"] for item in retrieved]
        chunks = chunk_repository.get_by_ids(chunk_ids)
        chunk_map = {chunk.chunk_id: chunk for chunk in chunks}

        ordered_contexts: list[str] = []
        citations_payload: list[QueryCitationResponse] = []
        citations_to_save: list[QueryCitation] = []

        query_id = str(uuid4())
        for rank, item in enumerate(retrieved, start=1):
            chunk = chunk_map.get(item["chunk_id"])
            if chunk is None:
                continue
            ordered_contexts.append(chunk.text)
            citations_payload.append(
                QueryCitationResponse(
                    chunk_id=chunk.chunk_id,
                    rank=rank,
                    score=float(item["score"]),
                    source_type=chunk.source_type,
                    source_url=chunk.source_url,
                    excerpt=chunk.text[:240],
                )
            )
            citations_to_save.append(
                QueryCitation(
                    query_citation_id=str(uuid4()),
                    query_id=query_id,
                    chunk_id=chunk.chunk_id,
                    rank=rank,
                    score=float(item["score"]),
                )
            )

        answer_text = generator.generate_answer(question=query_text, contexts=ordered_contexts)

        saved_query = query_repository.save_query(
            Query(
                query_id=query_id,
                user_id=report.user_id,
                report_id=target_report_id,
                query_text=query_text,
                answer_text=answer_text,
            )
        )
        query_repository.save_citations(citations_to_save)

        return QueryResponse(
            query_id=saved_query.query_id,
            report_id=saved_query.report_id,
            answer=saved_query.answer_text or "",
            citations=citations_payload,
        )

    def _retriever(self) -> Retriever:
        if self.retriever is None:
            self.retriever = Retriever()
        return self.retriever

    def _generator(self) -> AnswerGenerator:
        if self.generator is None:
            self.generator = AnswerGenerator()
        return self.generator

    def _resolve_latest_report_id(self) -> str:
        latest = report_repository.get_latest_for_user(settings.default_local_user_id)
        if latest is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No reports available. Upload a report first.",
            )
        return latest.report_id


query_service = QueryService()
