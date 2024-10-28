import logging

from domain import database, entities, dto


class SQLiteDB(database.Database):
    def __init__(self):
        self._logger = logging.getLogger('sqlite_db')
    def search(self, query: dto.VectorSearchQuery) -> dto.SearchResult:
        pass

    def insert(self, image: entities.Image) -> None:
        self._logger.info(f'inserting image {image.filepath}')