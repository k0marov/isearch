from domain import search_service, dto


class SearchServiceImpl(search_service.SearchService):
    def Search(self, query: dto.SearchQuery) -> dto.SearchResult:
        # TODO: implement me
        return dto.SearchResult(filenames=['test', 'test2', 'test3'])