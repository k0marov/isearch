import abc


class CLIExecutor(abc.ABC):
    @abc.abstractmethod
    async def execute(self, args: list[str]) -> int:
        pass
