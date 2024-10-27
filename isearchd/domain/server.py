import abc

from domain import config


class SocketServer(abc.ABC):
    @abc.abstractmethod
    def Start(self, cfg: config.Config) -> None:
        pass