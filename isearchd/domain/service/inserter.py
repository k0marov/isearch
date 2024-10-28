import logging
import os.path

from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import watchdog.events


from domain import database, entities, embedder
from domain.inserter_service import  InserterService

class InotifyInserterService(InserterService):
    def __init__(self, logger: logging.Logger, dir_path: str, db: database.Database, emb: embedder.Embedder):
        self._logger = logger
        self._dir_path = dir_path
        self._db = db
        self._emb = emb
        self._logger = logger

    def _handle_event(self, event: FileSystemEvent) -> None:
        self._logger.info(f'got event {event}')
        img_path = event.dest_path
        try:
            img = Image.open(img_path)
            img.load()
        except Exception as e:
            # self._logger.debug(f'failed opening file as image: {e}')
            return
        self._insert_image(img_path, img)

    def _insert_image(self, path: str, img: Image.Image):
        embedding = self._emb.generate_embedding_image(img)
        self._db.insert(entities.Image(filepath=path, emb=embedding))


    async def start(self) -> None:
        class Handler(FileSystemEventHandler):
            def on_any_event(self_, event: FileSystemEvent) -> None:
                self._handle_event(event)

        observer = Observer()
        observer.schedule(Handler(), self._dir_path, recursive=True, event_filter=(
            watchdog.events.FileCreatedEvent,
            watchdog.events.FileMovedEvent,
            watchdog.events.FileModifiedEvent,
        ))

        self._logger.info(f'started watching {self._dir_path}')

        observer.start()