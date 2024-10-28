import logging

from domain import database, entities, dto


class SQLiteDB(database.Database):
    def __init__(self, logger: logging.Logger):
        self._logger = logger
    def search(self, query: dto.VectorSearchQuery) -> dto.SearchResult:
        pass

    def insert(self, image: entities.Image) -> None:
        self._logger.info(f'inserting image {image.filepath}')