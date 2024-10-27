import dataclasses


@dataclasses.dataclass
class Embedding:
    data: bytes # TODO: use correct type

@dataclasses.dataclass
class VectorSearchQuery:
    embedding: Embedding

@dataclasses.dataclass
class SearchQuery:
    text: str

@dataclasses.dataclass
class SearchResult:
    filenames: list[str]