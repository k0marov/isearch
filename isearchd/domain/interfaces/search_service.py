"""Module with interface for main searching service."""
import abc

from domain import dto


class SearchService(abc.ABC):
    """A search service which should perform semantic search with a text query."""
    @abc.abstractmethod
    async def search(self, query: dto.SearchQuery) -> dto.SearchResult:
        """Perform semantic search using a text query."""
        pass
