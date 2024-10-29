from progress.bar import Bar

from domain.executor import CLIExecutor
from domain.provider import SearchProvider, SearchQuery
from domain.config import Config



HELP_MSG = \
'''Usage: isearch [OPTIONS] [QUERY]
Semantic image search CLI 

Options: 
    -h, --help             show this help 
    --info                 print config info 
    --reindex DIR          trigger reindexing for selected dir 
    -n INT                 specify amount of pictures to get. Defaults to 10 
'''

class CLIExecutorImpl(CLIExecutor):
    def __init__(self, cfg: Config, provider: SearchProvider) -> None:
        self._cfg = cfg
        self._provider = provider

    def _help(self):
        print(HELP_MSG)

    def _info(self):
        print(f'Connecting to isearchd socket: {self._cfg.socket_path}')

    async def execute(self, args: list[str]) -> None:
        if not args:
            return self._help()
        if args[0] == '--info':
            self._info()
            return
        elif args[0] == '--reindex' and len(args) > 1:
            await self._reindex(args[1])
            return

        return await self._search(args)

    async def _reindex(self, dir: str) -> None:
        progress_gen = self._provider.reindex(dir)
        bar = Bar('Reindexing', suffix='%(index)d/%(max)d %(elapsed_td)s - %(eta_td)s')
        async for curr, total in progress_gen:
            bar.max = total
            bar.next()

        bar.finish()


    async def _search(self, args: list[str]) -> None:
        count = None
        if args[0] == '-n':
            count = int(args[1])
            args = args[2:]
        query = SearchQuery(n=count, text=' '.join(args))
        results = await self._provider.search(query)
        for filepath in results.filepaths:
            print(filepath)