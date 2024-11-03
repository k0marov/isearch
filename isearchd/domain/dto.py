"""Module with DTOs needed for domain logic."""
from typing import Annotated, Literal
import dataclasses

import numpy as np

CLIP_EMBEDDING_SIZE = 640
CLIPEmbeddingType = Annotated[np.array, Literal[640]]


@dataclasses.dataclass
class Embedding:
    """DTO for embedding."""
    data: CLIPEmbeddingType


@dataclasses.dataclass
class VectorSearchQuery:
    """DTO for performing a vector search query."""
    embedding: Embedding
    count: int


@dataclasses.dataclass
class SearchQuery:
    """DTO for performing a search query."""
    text: str
    count: int


@dataclasses.dataclass
class SearchResult:
    """DTO for returning serach results."""
    filepaths: list[str]

