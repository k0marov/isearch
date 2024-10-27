import abc

class SocketServer(abc.ABC):
    @abc.abstractmethod
    async def Start(self) -> None:
        pass