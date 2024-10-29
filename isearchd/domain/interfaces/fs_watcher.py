import abc

class FSWatcher(abc.ABC):
    @abc.abstractmethod
    def start(self) -> None:
        pass