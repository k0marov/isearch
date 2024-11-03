"""Module with interface for the main inserter service."""
import abc
import typing


class InserterService(abc.ABC):
    """Service which should handle FS-related stuff such as reading pillow images."""
    @abc.abstractmethod
    def handle_image_upd_or_create(self, dir: str, filepath: str) -> None:
        """
        Handles an event when an image should be inserted for indexing.
        Args:
            dir: the directory from which this event was obtained (it is not always os.path.dirname, the file may be nested
            filepath: the filepath to the image. If it's not an image, the request is ignored.
        """
        pass

    @abc.abstractmethod
    def handle_deletion(self, filepath: str):
        """
        Handles an event when a file was deleted in watched dir. Removes it from the index.
        Args:
            filepath: path to a file that was deleted. If it was not indexed, the request is ignored.
        """
        pass

    @abc.abstractmethod
    def reindex_full(self, dir: str) -> typing.Generator[tuple[int, int], None, None]:
        """
        Performs full reindex of selected dir. Deletes all indexes for it, and then inserts all images one-by-one.
        The subdirectories are handled recursively by os.walk.
        Args:
            dir: path to the dir to index. It may be a watched dir, but also may be any directory.

        Returns:
            Generator, which yields two ints: "curr" and "total", representing the progress of the insertion.
            "curr" - the amount of files already added to index.
            "total" - total amount of files in dir.
        """
        pass
