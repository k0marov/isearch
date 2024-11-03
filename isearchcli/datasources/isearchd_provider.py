"""Module with implementation of isearchd wrapper using sockets."""
import asyncio

from domain.interfaces.provider import DaemonProvider, SearchQuery, SearchResult

PREFIX_LENGTH = 4
RECV_SIZE = 1024
DEFAULT_IMAGE_COUNT = 10

class DaemonProviderImpl(DaemonProvider):
    def __init__(self, socket_addr: str) -> None:
        self._socket_addr = socket_addr

    async def search(self, query: SearchQuery) -> SearchResult:
        reader, writer = await asyncio.open_unix_connection(self._socket_addr)

        count = query.n or DEFAULT_IMAGE_COUNT
        to_send = f'search:{count}:{query.text}'.encode()
        writer.write(len(to_send).to_bytes(PREFIX_LENGTH, byteorder='big'))
        writer.write(to_send)
        await writer.drain()

        result = ''
        while data := await reader.read(RECV_SIZE):
            result += data.decode()

        writer.close()
        await writer.wait_closed()

        return SearchResult(filepaths=result.split('\n'))

