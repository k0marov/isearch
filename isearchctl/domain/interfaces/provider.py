import abc
import typing

class DaemonProvider(abc.ABC):
    @abc.abstractmethod
    async def reindex(self, dir: str) -> typing.AsyncGenerator[tuple[int, int], None]:
        pass
