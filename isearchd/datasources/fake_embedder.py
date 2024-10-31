"""Module with stub implementation of domain's Embedder needed for tests."""
import logging

import numpy.random
from PIL import Image

from domain import dto
from domain.interfaces import embedder


class FakeEmbedder(embedder.Embedder):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def generate_embedding_text(self, _: str) -> dto.Embedding:
        return dto.Embedding(data=numpy.random.random(size=(1, dto.CLIP_EMBEDDING_SIZE)))

    def generate_embedding_image(self, _: Image.Image) -> dto.Embedding:
        return dto.Embedding(data=numpy.random.random(size=(1, dto.CLIP_EMBEDDING_SIZE)))
