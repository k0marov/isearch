import abc
import typing


class InserterService(abc.ABC):
    @abc.abstractmethod
    def handle_image_upd_or_create(self, dir: str, filepath: str) -> None:
        pass

    @abc.abstractmethod
    def handle_deletion(self, filepath: str):
        pass

    @abc.abstractmethod
    def reindex_full(self, dir: str) -> typing.Generator[tuple[int, int], None, None]:
        pass