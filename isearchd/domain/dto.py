import dataclasses
import numpy as np


@dataclasses.dataclass
class Embedding:
    data: np.array

@dataclasses.dataclass
class VectorSearchQuery:
    embedding: Embedding

@dataclasses.dataclass
class SearchQuery:
    text: str

@dataclasses.dataclass
class SearchResult:
    filenames: list[str]