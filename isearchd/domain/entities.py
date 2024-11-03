"""Module with main domain entities."""
from dataclasses import dataclass

from domain import dto


@dataclass
class Image:
    """Main entity - Image.
    watched_dir - is a directory from which this image was indexed.
        It is not just equal to os.path.basedir(filepath), the file may be nested in a subdir in it,
        since we watch directories recursively.
    """
    filepath: str
    watched_dir: str
    emb: dto.Embedding

