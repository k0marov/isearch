"""Module with real implementation for domain's Database - a wrapper around SQLite3."""
import logging
import os.path

import numpy as np
import aiosqlite
import sqlite_vec


from domain import entities, dto
from domain.interfaces import database

class SQLiteDB(database.Database):
    def __init__(self, logger: logging.Logger, db_path: str):
        self._logger = logger
        self._db_path = db_path

    async def init_db(self) -> None:
        """Initialize database, load extensions, apply migrations."""
        self._logger.info(f'initializing db at {self._db_path}...')
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._db = await aiosqlite.connect(self._db_path)
        await self._db.enable_load_extension(True)
        await self._db.load_extension(sqlite_vec.loadable_path())
        # await sqlite_vec.load(self._db)
        await self._db.enable_load_extension(False)

        await self._migrate()

    async def _migrate(self):
        self._logger.info('migrating db...')
        await self._db.execute(
            '''create table if not exists images (
                filepath varchar PRIMARY KEY,
                dir varchar,
                embedding float[{0}] check(
                  typeof(embedding) == 'blob'
                  and vec_length(embedding) == {0}
                )
            )'''.format(dto.CLIP_EMBEDDING_SIZE)  # it's not an SQL injection since it's our constant
        )
        await self._db.commit()

    async def search(self, query: dto.VectorSearchQuery) -> dto.SearchResult:
        self._logger.info('performing vector search in sqlite')
        args = {
            'emb': query.embedding.data.astype(np.float32),
            'count': query.count
        }
        async with self._db.execute('''
            select
              dir,
              filepath,
              vec_distance_L1(embedding, :emb) as distance
            from images
            order by distance
            limit :count;
        ''', args) as cursor:
            rows = await cursor.fetchall()
            return dto.SearchResult(filepaths=[filepath for _, filepath, _ in rows])

    async def update_or_create(self, image: entities.Image) -> None:
        self._logger.info(f'update_or_create image row at {image.filepath}')
        await self._db.execute('''
            insert into images values (
               :filepath, :dir, :embedding
            )
            on conflict(filepath)
            do update set
                dir=excluded.dir,
                embedding=excluded.embedding
        ''', {
            'filepath': image.filepath,
            'dir': image.watched_dir,
            'embedding': image.emb.data.astype(np.float32),
        })
        await self._db.commit()

    async def delete(self, filepath: str) -> None:
        self._logger.info(f'deleting image at {filepath}')
        await self._db.execute('delete from images where filepath = ?', (filepath,))
        await self._db.commit()

    async def clear_dir_embeddings(self, dir: str) -> None:
        self._logger.info(f'deleting all dir={dir} images from db')
        await self._db.execute('delete from images where dir = ?', (dir,))
        await self._db.commit()
