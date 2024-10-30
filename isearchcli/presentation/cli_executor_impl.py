from domain.interfaces.executor import CLIExecutor
from domain.interfaces.provider import DaemonProvider, SearchQuery
from domain.config import Config


HELP_MSG = \
    '''Usage: isearch [OPTIONS] [QUERY]
Semantic image search CLI.
Depends on a daemon running in the background. See isearchd

Options:
    -h, --help             show this help
    --info                 print config info
    --reindex DIR          trigger reindexing for selected dir
    -n INT                 specify amount of pictures to get. Defaults to 10
'''


class CLIExecutorImpl(CLIExecutor):
    def __init__(self, cfg: Config, provider: DaemonProvider) -> None:
        self._cfg = cfg
        self._provider = provider

    def _help(self):
        print(HELP_MSG)

    def _info(self):
        print(f'Connecting to isearchd socket: {self._cfg.socket_path}')

    async def execute(self, args: list[str]) -> None:
        if not args or args[0] == '-h':
            return self._help()
        elif args[0] == '--info':
            self._info()
            return

        return await self._search(args)

    async def _search(self, args: list[str]) -> None:
        count = None
        if args[0] == '-n':
            count = int(args[1])
            args = args[2:]
        query = SearchQuery(n=count, text=' '.join(args))
        results = await self._provider.search(query)
        for filepath in results.filepaths:
            print(filepath)

