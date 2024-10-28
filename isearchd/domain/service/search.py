from domain import search_service, dto, database, embedder


class SearchServiceImpl(search_service.SearchService):
    def __init__(self, db: database.Database, emb: embedder.Embedder):
        self._db = db
        self._emb = emb
    def search(self, query: dto.SearchQuery) -> dto.SearchResult:
        text_emb = self._emb.generate_embedding_text(query.text)
        return dto.SearchResult(filenames=['test', str(text_emb.data)])
        # return self._db.search(dto.VectorSearchQuery(embedding=text_emb))