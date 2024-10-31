"""Module with stub implementation of domain's Embedder needed for tests."""
import logging

import numpy.random
from PIL import Image

from domain import dto
from domain.interfaces import embedder


class StubEmbedder(embedder.Embedder):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def generate_embedding_text(self, text: str) -> dto.Embedding:
        self._logger.info(f'got request for generating embedding for text: {text}')
        self._logger.info(f'returning random data')
        return dto.Embedding(data=numpy.random.random(size=(1, dto.CLIP_EMBEDDING_SIZE)))

    def generate_embedding_image(self, img: Image.Image) -> dto.Embedding:
        self._logger.info(f'got request for generating embedding for an image')
        self._logger.info(f'returning random data')
        return dto.Embedding(data=numpy.random.random(size=(1, dto.CLIP_EMBEDDING_SIZE)))
