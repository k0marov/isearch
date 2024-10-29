import asyncio
import sys
import di
from domain import config

async def main():
    cfg = config.Config(socket_path=config.get_socket_path())
    executor = di.Init(cfg)
    await executor.execute(sys.argv[1:])

if __name__ == '__main__':
    asyncio.run(main())