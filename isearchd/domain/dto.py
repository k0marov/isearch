import dataclasses

import numpy as np


# TODO: place embedding size constant here

@dataclasses.dataclass
class Embedding:
    """DTO for embedding."""
    data: np.array


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
