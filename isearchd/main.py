import asyncio
import logging

from api import server_impl
from datasources import clip_embedder, database
from domain import config
from domain.service import search, inserter


async def main():
    logger = logging.getLogger('isearch')
    logger.setLevel(logging.DEBUG)
    cfg = config.Config(
        socket_path=config.get_socket_path(),
        db_path=config.get_db_path(),
        img_dir=config.get_default_watching_dir(),
    )
    db = database.SQLiteDB(logger=logger.getChild('database'))

    embedder = clip_embedder.CLIPEmbedder(logger=logger.getChild('embedder'))
    searcher = search.SearchServiceImpl(logger=logger.getChild('searcher'), db=db, emb=embedder)
    image_inserter = inserter.InotifyInserterService(logger=logger.getChild('inserter'), dir_path=cfg.img_dir, db=db, emb=embedder)

    server = server_impl.SocketServerImpl(logger.getChild('server'), cfg, searcher)

    await asyncio.gather(server.start(), image_inserter.start())


if __name__ == '__main__':
    asyncio.run(main())