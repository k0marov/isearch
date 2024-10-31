import abc


class CLIExecutor(abc.ABC):
    """Abstraction for parsing arguments and executing the commands."""
    @abc.abstractmethod
    async def execute(self, args: list[str]) -> None:
        """
        Parses provided cmd args and executes the wanted action.
        Args:
            args: list of bash args, omitting the program name (starts from 1).
        """
        pass
