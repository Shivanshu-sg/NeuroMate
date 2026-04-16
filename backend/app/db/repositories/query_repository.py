from app.db.session import SessionLocal
from app.models.query import Query
from app.models.query_citation import QueryCitation


class QueryRepository:
    def save_query(self, query: Query) -> Query:
        with SessionLocal() as session:
            persisted = session.merge(query)
            session.commit()
            session.refresh(persisted)
            session.expunge(persisted)
            return persisted

    def save_citations(self, citations: list[QueryCitation]) -> list[QueryCitation]:
        if not citations:
            return []
        with SessionLocal() as session:
            session.add_all(citations)
            session.commit()
            for citation in citations:
                session.refresh(citation)
                session.expunge(citation)
            return citations


query_repository = QueryRepository()
