from progress.bar import Bar

from domain.interfaces.executor import CLIExecutor
from domain.interfaces.provider import DaemonProvider
from domain.config import Config


HELP_MSG = \
    '''Usage: isearchctl [OPTIONS] SUBCOMMAND
Configuration and management utility for isearch system.

Options:
    -h, --help             show this help
    --info                 print config info

Subcommands:
    reindex DIR            trigger reindexing for DIR
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
        if not args:
            return self._help()
        if args[0] == '--info':
            self._info()
        elif args[0] == 'reindex' and len(args) > 1:
            await self._reindex(args[1])
        else:
            self._help()

    async def _reindex(self, dir: str) -> None:
        progress_gen = self._provider.reindex(dir)
        bar = Bar('Reindexing',
                  suffix='%(index)d/%(max)d %(elapsed_td)s - %(eta_td)s')
        async for curr, total in await progress_gen:
            bar.index = curr
            bar.max = total

        bar.finish()

