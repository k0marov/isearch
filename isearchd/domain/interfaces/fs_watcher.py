"""Module with interface for the component that monitors fs events."""
import abc


class FSWatcher(abc.ABC):
    """Responsible for subscribing to FS events and passing them to InserterService"""
    @abc.abstractmethod
    async def start(self) -> None:
        """Starts listening for events."""
        pass

