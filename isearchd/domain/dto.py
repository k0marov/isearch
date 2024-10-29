import dataclasses
import typing

import numpy as np


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
    count: typing.Optional[int]

@dataclasses.dataclass
class SearchResult:
    filepaths: list[str]