import asyncio
import typing

from domain.provider import DaemonProvider

RECV_SIZE = 1024

class DaemonProviderImpl(DaemonProvider):
    def __init__(self, socket_addr: str) -> None:
        self._socket_addr = socket_addr

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