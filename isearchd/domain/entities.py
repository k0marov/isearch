from dataclasses import dataclass

from domain import dto


@dataclass
class Image:
    filepath: str
    emb: dto.Embedding