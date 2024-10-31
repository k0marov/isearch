"""Module with interface for a wrapper for DB that is required for business logic."""
import abc

from domain import dto, entities


class Database(abc.ABC):
    """Database wrapper for persisting embeddings.
    It must support parallel READs. Parallel WRITEs are not required.
    """
    @abc.abstractmethod
    def search(self, query: dto.VectorSearchQuery) -> dto.SearchResult:
        """
        Perform a vector search through indexed files.
        Args:
            query: embedding and other params for search.

        Returns:
            list of results
        """
        pass

    @abc.abstractmethod
    def update_or_create(self, image: entities.Image) -> None:
        """
        Inserts an image along with its embedding into db.
        If image is already indexed, updates it's embedding.
        Args:
            image: entity to insert
        """
        pass

    @abc.abstractmethod
    def delete(self, filepath: str) -> None:
        """
        Deletes an index for the image at provided filepath.
        If it was not indexed, does nothing.
        Args:
            filepath: path used for identifying the image.
        """
        pass

    @abc.abstractmethod
    def clear_dir_embeddings(self, dir: str) -> None:
        """
        Deletes ALL embeddings for images from the selected directory.
        Args:
            dir: path to dir for deleting embeddings.
        """
        pass
