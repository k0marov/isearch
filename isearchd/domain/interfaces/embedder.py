"""Module with interface for a wrapper for ML embedding model."""
import abc

from PIL.Image import Image

from domain import dto


class Embedder(abc.ABC):
    """Wrapper around CLIP.
    Responsible for instantiating ML model and generating embeddings through it"""
    @abc.abstractmethod
    def generate_embedding_text(self, text: str) -> dto.Embedding:
        """
        Generates embedding for text string.
        Args:
            text: text to generate embedding for

        Returns:
            embedding that can be used for semantic search
        """
        pass

    @abc.abstractmethod
    def generate_embedding_image(self, img: Image) -> dto.Embedding:
        """
        Generates embedding for an image.
        Args:
            img: pillow image

        Returns:
            embedding that can be used for semantic search
        """
        pass

