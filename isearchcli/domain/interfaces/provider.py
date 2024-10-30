import abc
import typing
from dataclasses import dataclass


@dataclass
class SearchQuery:
    text: str
    n: typing.Optional[int]


@dataclass
class SearchResult:
    filepaths: list[str]


class DaemonProvider(abc.ABC):
    @abc.abstractmethod
    async def search(self, query: SearchQuery) -> SearchResult:
        pass

