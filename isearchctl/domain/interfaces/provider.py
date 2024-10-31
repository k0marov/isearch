import abc
import typing


class DaemonProvider(abc.ABC):
    """Wrapper for isearchd api"""
    @abc.abstractmethod
    def reindex(self, dir: str) -> typing.AsyncGenerator[tuple[int, int], None]:
        """
        Executes reindex for the provided $dir in isearchd.
        Args:
            dir: directory path for which to execute reindex.

        Returns:
            Async generator that in realtime yields two ints: curr and total.
            total is the total number of files in provided dir (recursively)
            curr is the number for which indexing is already finished.
        """
        pass
