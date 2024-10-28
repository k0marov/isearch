import numpy as np
import logging

import sqlite3
import sqlite_vec


from domain import database, entities, dto

EMBEDDING_SHAPE = 640

class SQLiteDB(database.Database):
    def __init__(self, logger: logging.Logger, db_path: str):
        self._logger = logger
        self._db = sqlite3.connect(db_path, check_same_thread=False) # we don't write concurrently, so it's ok to switch this to False
        self._db.enable_load_extension(True)
        sqlite_vec.load(self._db)
        self._db.enable_load_extension(False)

        self._migrate()

    def _migrate(self):
        self._db.execute(
            '''create table if not exists images (
                filepath varchar PRIMARY KEY, 
                dir varchar, 
                emb float[{}]
            )'''.format(EMBEDDING_SHAPE) # it's not an SQL injection since its our constant
        )

    def search(self, query: dto.VectorSearchQuery) -> dto.SearchResult:
        pass

    def insert(self, image: entities.Image) -> None:
        self._logger.info(f'inserting image {image.filepath}')
        self._db.execute('''
            insert into images values (
               :dir, :filepath, :emb 
            )
        ''', {
            'dir': 'default_dir',
            'filepath': image.filepath,
            'emb': image.emb.data.astype(np.float32),
        })