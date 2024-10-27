import abc


class CLIExecutor(abc.ABC):
    @abc.abstractmethod
    def execute(self, args: list[str]) -> int:
        pass
