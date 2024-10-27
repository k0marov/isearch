import abc

class InserterService(abc.ABC):
    @abc.abstractmethod
    async def Start(self) -> None:
        pass