from dataclasses import dataclass

from domain import dto


@dataclass
class Image:
    filepath: str
    watched_dir: str
    emb: dto.Embedding