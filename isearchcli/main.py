import asyncio
import sys
import di
from domain import config

async def _main():
    cfg = config.get_config_from_env()
    executor = di.Init(cfg)
    await executor.execute(sys.argv[1:])

if __name__ == '__main__':
    asyncio.run(_main())