import asyncio
import logging

from domain import config, dto
from domain.interfaces import search_service
from domain.interfaces.inserter_service import InserterService
from domain.interfaces.server import SocketServer

RECV_SIZE = 1024


class SocketServerImpl(SocketServer):
    def __init__(self, logger: logging.Logger, cfg: config.Config, searcher: search_service.SearchService, inserter: InserterService):
        self._cfg = cfg
        self._logger = logger
        self._searcher = searcher
        self._inserter = inserter

    async def start(self) -> None:
        server = await asyncio.start_unix_server(self._handler, self._cfg.socket_path)
        async with server:
            self._logger.info('Server running...')
            await server.serve_forever()

    async def _handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        MESSAGE_LENGTH_PREFIX = 4
        message_length_bytes = await reader.read(MESSAGE_LENGTH_PREFIX)
        message_length = int.from_bytes(message_length_bytes, byteorder='big')

        input = (await reader.read(message_length)).decode()

        self._logger.debug(f'got message "{input}"')
        if input.startswith('search:'):  # search:5:prompt
            count, text = input.removeprefix('search:').split(':', maxsplit=1)
            query = dto.SearchQuery(text=text, count=int(count))
            output = '\n'.join(self._searcher.search(query).filepaths)
            self._logger.debug(f'answering with "{output}"')
            writer.write(output.encode())
        elif input.startswith('reindex:'):
            dir = input.removeprefix('reindex:')
            self._logger.info(
                'performing reindex because of socket request', extra={'dir': dir})
            for curr_progress, total in self._inserter.reindex_full(dir):
                writer.write(f'{curr_progress}/{total}\n'.encode())
        else:
            writer.write('error:unknown cmd'.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
