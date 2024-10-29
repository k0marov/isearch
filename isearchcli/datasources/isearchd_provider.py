import asyncio
import socket
import typing

from domain.provider import SearchProvider, SearchQuery, SearchResult

RECV_SIZE = 1024

class SearchProviderImpl(SearchProvider):
    def __init__(self, socket_addr: str) -> None:
        self._socket_addr = socket_addr

    def search(self, query: SearchQuery) -> SearchResult:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(self._socket_addr)

        to_send = f'search:{query.text}'
        client.send(to_send.encode())
        result = ''
        while data := client.recv(RECV_SIZE):
            result += data.decode()

        client.close()
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