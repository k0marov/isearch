"""Module with implementation for the SearchService."""
import logging

from domain import dto
from domain.interfaces import database, embedder, search_service


class SearchServiceImpl(search_service.SearchService):
    def __init__(self, logger: logging.Logger, db: database.Database, emb: embedder.Embedder):
        self._logger = logger
        self._db = db
        self._emb = emb

    def search(self, query: dto.SearchQuery) -> dto.SearchResult:
        text_emb = self._emb.generate_embedding_text(query.text)
        return self._db.search(dto.VectorSearchQuery(embedding=text_emb, count=query.count))
