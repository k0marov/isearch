from isearchcli.domain.executor import CLIExecutor
from isearchcli.domain.provider import SearchProvider


class CLIExecutorImpl(CLIExecutor):
    def __init__(self, provider: SearchProvider) -> None:
        self._provider = provider

    def execute(self, args: list[str]) -> None:
        # TODO: implement me
        pass
