from domain.provider import SearchProvider, SearchQuery, SearchResult


class SearchProviderImpl(SearchProvider):
    def __init__(self) -> None:
        pass

    def search(self, query: SearchQuery) -> SearchResult:
        # TODO: implement me
        return SearchResult(filepaths=['hello', 'test', 'test123'])
