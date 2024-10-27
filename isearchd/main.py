import asyncio
import logging

from api import server_impl
from domain import config
from domain.service import search


async def main():
    logging.getLogger().setLevel(logging.DEBUG)
    searcher = search.SearchServiceImpl()
    cfg = config.Config(socket_path=config.get_socket_path())
    server = server_impl.SocketServerImpl(cfg, searcher)

    server_task = server.Start()
    await asyncio.gather(server_task)


if __name__ == '__main__':
    asyncio.run(main())