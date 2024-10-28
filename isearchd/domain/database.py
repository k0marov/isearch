import abc

from domain import dto, entities


class Database(abc.ABC):
    @abc.abstractmethod
    def search(self, query: dto.VectorSearchQuery) -> dto.SearchResult:
        pass
    @abc.abstractmethod
    def insert(self, image: entities.Image) -> None:
        pass