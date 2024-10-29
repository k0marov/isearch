import asyncio
import socket
import typing

from domain.provider import SearchProvider, SearchQuery, SearchResult

RECV_SIZE = 1024
DEFAULT_IMAGE_COUNT = 10

class SearchProviderImpl(SearchProvider):
    def __init__(self, socket_addr: str) -> None:
        self._socket_addr = socket_addr

    async def search(self, query: SearchQuery) -> SearchResult:
        reader, writer = await asyncio.open_unix_connection(self._socket_addr)

        count = query.n or DEFAULT_IMAGE_COUNT
        to_send = f'search:{count}:{query.text}'
        writer.write(to_send.encode())

        result = ''
        while data := await reader.read(RECV_SIZE):
            result += data.decode()

        writer.close()
        await writer.wait_closed()

        return SearchResult(filepaths=result.split('\n'))

    async def reindex(self, dir: str) -> typing.AsyncGenerator[tuple[int, int], None]:
        reader, writer = await asyncio.open_unix_connection(self._socket_addr)

        to_send = f'reindex:{dir}'
        writer.write(to_send.encode())
        await writer.drain()

        while (progress := await reader.readuntil('\n'.encode())):
            curr, total = map(int, progress.decode().split('/'))
            yield curr, total
            if curr == total:
                break

        writer.close()
        await writer.wait_closed()