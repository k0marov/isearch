"""Module with configuration utilities."""
import os
from dataclasses import dataclass

DEFAULT_SOCKET = '~/.cache/isearch/isearchd.sock'

@dataclass
class Config:
    socket_path: str

def get_config_from_env() -> Config:
    return Config(
        socket_path=os.getenv('ISEARCHD_SOCKET') or os.path.expanduser(DEFAULT_SOCKET),
    )
