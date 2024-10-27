import socket
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
