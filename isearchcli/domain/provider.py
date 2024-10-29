import abc
import asyncio
import typing
from dataclasses import dataclass


@dataclass
class SearchQuery:
    text: str


@dataclass
class SearchResult:
    filepaths: list[str]


class SearchProvider(abc.ABC):
    @abc.abstractmethod
    def search(self, query: SearchQuery) -> SearchResult:
        pass

    @abc.abstractmethod
    async def reindex(self, dir: str) -> typing.AsyncGenerator[tuple[int, int], None]:
        pass
