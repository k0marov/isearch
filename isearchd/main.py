import asyncio
import logging

from api import server_impl
from datasources import clip_embedder
from domain import config
from domain.service import search


async def main():
    logging.getLogger().setLevel(logging.DEBUG)
    embedder = clip_embedder.CLIPEmbedder()
    searcher = search.SearchServiceImpl(db=None, emb=embedder)
    cfg = config.Config(socket_path=config.get_socket_path(), db_path=config.get_db_path())
    server = server_impl.SocketServerImpl(cfg, searcher)

    server_task = server.start()
    await asyncio.gather(server_task)


if __name__ == '__main__':
    asyncio.run(main())