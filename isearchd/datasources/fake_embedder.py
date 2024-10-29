import logging

import numpy
import numpy.random
from PIL import Image

from domain import dto
from domain.interfaces import embedder

class FakeEmbedder(embedder.Embedder):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def generate_embedding_text(self, text: str) -> dto.Embedding:
        return dto.Embedding(data=numpy.random.random(size=(1, 640)))

    def generate_embedding_image(self, img: Image.Image) -> dto.Embedding:
        return dto.Embedding(data=numpy.random.random(size=(1, 640)))