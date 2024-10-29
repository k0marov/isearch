import abc

from domain import dto


class SearchService(abc.ABC):
    @abc.abstractmethod
    def search(self, query: dto.SearchQuery) -> dto.SearchResult:
        pass
