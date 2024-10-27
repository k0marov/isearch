import abc

from domain import dto


class Embedder(abc.ABC):
    @abc.abstractmethod
    def generate_embedding_text(self, text: str) -> dto.Embedding:
        pass

    @abc.abstractmethod
    def generate_embedding_image(self, image_path: str) -> dto.Embedding:
        pass