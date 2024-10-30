import abc


class SocketServer(abc.ABC):
    @abc.abstractmethod
    async def start(self) -> None:
        pass

