import logging
import os.path

from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent, DirDeletedEvent, FileDeletedEvent
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
        img_path = event.dest_path if event.event_type == watchdog.events.EVENT_TYPE_MOVED else event.src_path
        try:
            img = Image.open(img_path)
            img.load()
        except Exception as e:
            self._logger.debug(f'failed opening file as image: {e}')
            return
        self._insert_image(img_path, img)

    def _handle_deletion(self, event: FileDeletedEvent) -> None:
        self._db.delete(event.src_path)

    def _insert_image(self, path: str, img: Image.Image) -> None:
        embedding = self._emb.generate_embedding_image(img)
        self._db.update_or_create(entities.Image(watched_dir=self._dir_path, filepath=path, emb=embedding))


    async def start(self) -> None:
        class Handler(FileSystemEventHandler):
            def on_any_event(_, event: FileSystemEvent) -> None:
                self._handle_event(event)
            def on_deleted(_, event: FileDeletedEvent) -> None:
                self._handle_deletion(event)
                pass

        observer = Observer()
        observer.schedule(Handler(), self._dir_path, recursive=True, event_filter=(
            watchdog.events.FileCreatedEvent,
            watchdog.events.FileMovedEvent,
            watchdog.events.FileModifiedEvent,
            watchdog.events.FileDeletedEvent,
        ))

        self._logger.info(f'started watching {self._dir_path}')

        observer.start()
        # TODO: properly close all resources