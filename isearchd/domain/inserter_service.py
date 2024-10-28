import abc

class InserterService(abc.ABC):
    @abc.abstractmethod
    async def start(self) -> None:
        pass