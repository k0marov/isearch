"""Module with interface for socket server."""
import abc


class SocketServer(abc.ABC):
    """A socket server which should handle :search and :reindex requests."""
    @abc.abstractmethod
    async def start(self) -> None:
        """Should block and start serving socket requests."""
        pass
