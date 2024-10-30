import dataclasses

import numpy as np


# TODO: place embedding size constant here

@dataclasses.dataclass
class Embedding:
    data: np.array


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

