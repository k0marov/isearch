import abc
import typing
from dataclasses import dataclass


@dataclass
class SearchQuery:
    """Dataclass that represents args for a text search query."""
    text: str
    n: typing.Optional[int]


@dataclass
class SearchResult:
    """Dataclass that represents result of semantic search through isearchd."""
    filepaths: list[str]


class DaemonProvider(abc.ABC):
    """Wrapper for isearchd api using sockets."""
    @abc.abstractmethod
    async def search(self, query: SearchQuery) -> SearchResult:
        """
        Perform semantic search.
        Args:
            query: args for search

        Returns:
            list of top matching files
        """
        pass

