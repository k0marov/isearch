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
                embedding float[{0}] check(
                  typeof(embedding) == 'blob'
                  and vec_length(embedding) == {0}
                )
            )'''.format(EMBEDDING_SHAPE) # it's not an SQL injection since it's our constant
        )

    def search(self, query: dto.VectorSearchQuery) -> dto.SearchResult:
        self._logger.info(f'performing vector search in sqlite')
        rows = self._db.execute('''
            select
              dir,
              filepath,
              vec_distance_L2(embedding, :emb) as distance
            from images
            order by distance
            limit 10;
        ''', {'emb': query.embedding.data.astype(np.float32)}).fetchall() # TODO: make 10 a variable
        return dto.SearchResult(filepaths=[filepath for _, filepath, _ in rows])

    def update_or_create(self, image: entities.Image) -> None:
        self._logger.info(f'update_or_create image row at {image.filepath}')
        self._db.execute('''
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
        self._db.commit()

    def delete(self, filepath: str) -> None:
        self._logger.info(f'deleting image at {filepath}')
        self._db.execute('delete from images where filepath = ?', (filepath,))
        self._db.commit()