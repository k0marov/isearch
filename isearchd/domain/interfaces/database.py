import abc

from domain import dto, entities


class Database(abc.ABC):
    @abc.abstractmethod
    def search(self, query: dto.VectorSearchQuery) -> dto.SearchResult:
        pass

    @abc.abstractmethod
    def update_or_create(self, image: entities.Image) -> None:
        pass

    @abc.abstractmethod
    def delete(self, filepath: str) -> None:
        pass

    @abc.abstractmethod
    def clear_dir_embeddings(self, dir: str) -> None:
        pass
