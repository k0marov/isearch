import logging
import os.path
import typing

from PIL import Image
from domain import database, entities, embedder
from domain.inserter_service import  InserterService

class InotifyInserterService(InserterService):
    def __init__(self, logger: logging.Logger, db: database.Database, emb: embedder.Embedder):
        self._logger = logger
        self._db = db
        self._emb = emb

    def handle_image_upd_or_create(self, dir: str, filepath: str) -> None:
        try:
            img = Image.open(filepath)
            img.load()
        except Exception as e:
            self._logger.debug(f'failed opening file as image: {e}')
            return
        embedding = self._emb.generate_embedding_image(img)
        self._db.update_or_create(entities.Image(watched_dir=dir, filepath=filepath, emb=embedding))

    def handle_deletion(self, filepath: str):
        self._db.delete(filepath)

    def reindex_full(self, dir: str) -> typing.Generator[tuple[int, int], None, None]:
        self._logger.info(f'performing full reindex for dir {dir}')
        self._db.clear_dir_embeddings(dir)
        total_files_count = sum([len(files) for _, _, files in os.walk(dir)])
        processed_count = 0
        for root, _, files in os.walk(dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                self._logger.info(f'found file for reindex at {filepath}')
                self.handle_image_upd_or_create(dir, filename)
                processed_count += 1
                yield processed_count, total_files_count