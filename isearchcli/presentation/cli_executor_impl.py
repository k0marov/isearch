from domain.executor import CLIExecutor
from domain.provider import SearchProvider, SearchQuery


class CLIExecutorImpl(CLIExecutor):
    def __init__(self, provider: SearchProvider) -> None:
        self._provider = provider

    def help(self):
        print('test help message')

    def execute(self, args: list[str]) -> None:
        if not args:
            return self.help()
        query = SearchQuery(text=args[0])
        results = self._provider.search(query)
        for filepath in results.filepaths:
            print(filepath)
