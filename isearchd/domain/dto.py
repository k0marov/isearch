from typing import Annotated, Literal, TypeVar
import dataclasses

import numpy as np

CLIP_EMBEDDING_SIZE = 640
CLIPEmbeddingType = Annotated[np.array, Literal[640]]


@dataclasses.dataclass
class Embedding:
    data: CLIPEmbeddingType


@dataclasses.dataclass
class VectorSearchQuery:
    embedding: Embedding
    count: int


@dataclasses.dataclass
class SearchQuery:
    text: str
    count: int


@dataclasses.dataclass
class SearchResult:
    filepaths: list[str]

