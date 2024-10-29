import abc

from PIL.Image import Image

from domain import dto


class Embedder(abc.ABC):
    @abc.abstractmethod
    def generate_embedding_text(self, text: str) -> dto.Embedding:
        pass

    @abc.abstractmethod
    def generate_embedding_image(self, img: Image) -> dto.Embedding:
        pass