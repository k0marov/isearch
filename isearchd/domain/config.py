import dataclasses
import os


@dataclasses.dataclass
class Config:
    socket_path: str

def get_socket_path() -> str:
    return os.getenv('ISEARCHD_SOCKET') or os.path.expanduser('~/.cache/isearch/isearchd.sock')