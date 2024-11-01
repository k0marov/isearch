"""Main entrypoint module for isearchd."""
import asyncio
import logging
import sys

from api import server_impl
from datasources import database, inotify_watcher
from domain import config
from domain.service import search, inserter
from domain.interfaces.embedder import Embedder
from domain import const


def _init_embedder(cfg: config.Config, logger: logging.Logger) -> Embedder:
    if cfg.is_integration_test:
        logger.info('initializing stub embedder for test environment...')
        from datasources import stub_embedder
        return stub_embedder.StubEmbedder(logger=logger)
    else:
        logger.info('initializing clip embedder for real environment...')
        from datasources import clip_embedder
        return clip_embedder.CLIPEmbedder(logger=logger)


async def _main():
    if sys.argv and sys.argv[1] in ('-h', '--help'):
        print(const.HELP_MSG)
        return
    cfg = config.get_config_from_env()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('isearch')
    if cfg.is_debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.info('initializing system...')
    logger.info(f'got config: {cfg}')

    db = database.SQLiteDB(logger=logger.getChild('database'), db_path=cfg.db_path)
    await db.init_db()
    embedder = _init_embedder(cfg, logger.getChild('embedder'))

    searcher = search.SearchServiceImpl(logger=logger.getChild('searcher'), db=db, emb=embedder)
    image_inserter = inserter.InotifyInserterService(logger=logger.getChild('inserter'), db=db, emb=embedder)
    watcher = inotify_watcher.InotifyWatcherImpl(
        logger=logger.getChild('inotify_watcher'),
        dir_path=cfg.img_dir,
        inserter=image_inserter
    )

    server = server_impl.SocketServerImpl(logger.getChild('server'), cfg, searcher, image_inserter)

    await asyncio.gather(server.start(), watcher.start())


if __name__ == '__main__':
    asyncio.run(_main())