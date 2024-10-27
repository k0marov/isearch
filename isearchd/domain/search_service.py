import abc

from domain import dto


class SearchService(abc.ABC):
    @abc.abstractmethod
    def Search(self, query: dto.SearchQuery) -> dto.SearchResult:
        pass
