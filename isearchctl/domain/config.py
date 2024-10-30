import os
from dataclasses import dataclass


@dataclass
class Config:
    socket_path: str


DEFAULT_SOCKET = '~/.cache/isearch/isearchd.sock'


def get_socket_path() -> str:
    return os.getenv('ISEARCHD_SOCKET') or os.path.expanduser(DEFAULT_SOCKET)
