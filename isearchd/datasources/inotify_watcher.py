import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent, FileDeletedEvent
import watchdog.events

from domain.interfaces.fs_watcher import  FSWatcher
from domain.interfaces.inserter_service import InserterService

class InotifyWatcherImpl(FSWatcher):
    def __init__(self, logger: logging.Logger, dir_path: str, inserter: InserterService):
        self._logger = logger
        self._dir_path = dir_path
        self._inserter = inserter

    async def start(self) -> None:
        class Handler(FileSystemEventHandler):
            def on_any_event(_, event: FileSystemEvent) -> None:
                self._logger.info(f'got event {event}')
            def on_created(_, event: FileSystemEvent) -> None:
                self._inserter.handle_image_upd_or_create(self._dir_path, event.src_path)
            def on_modified(_, event: FileSystemEvent) -> None:
                self._inserter.handle_image_upd_or_create(self._dir_path, event.src_path)
            def on_moved(_, event: FileSystemEvent) -> None:
                self._inserter.handle_image_upd_or_create(self._dir_path, event.dest_path)
                self._inserter.handle_deletion(event.src_path)
            def on_deleted(_, event: FileDeletedEvent) -> None:
                self._inserter.handle_deletion(event.src_path)

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