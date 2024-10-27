from domain.executor import CLIExecutor
from domain.provider import SearchProvider, SearchQuery
from domain.config import Config


HELP_MSG = \
'''Usage: isearch [OPTIONS] QUERY 
Semantic image search CLI 

Options: 
    -h, --help      show this help 
    --info          print config info 
'''

class CLIExecutorImpl(CLIExecutor):
    def __init__(self, cfg: Config, provider: SearchProvider) -> None:
        self._cfg = cfg
        self._provider = provider

    def _help(self):
        print(HELP_MSG)

    def _info(self):
        print(f'Connecting to isearchd socket: {self._cfg.socket_path}')

    def execute(self, args: list[str]) -> None:
        if not args:
            return self._help()
        if args[0].startswith('-'):
            if args[0] == '--info':
                self._info()
            else:
                self._help()
            return
        return self._search(args[0])

    def _search(self, text: str) -> None:
        query = SearchQuery(text=text)
        results = self._provider.search(query)
        for filepath in results.filepaths:
            print(filepath)