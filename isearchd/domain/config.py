import dataclasses
import os


@dataclasses.dataclass
class Config:
    socket_path: str
    db_path: str
    img_dir: str
    is_debug: bool


DEFAULT_SOCKET = '~/.cache/isearch/isearchd.sock'
DEFAULT_DB = '~/.cache/isearch/db.sqlite3'
DEFAULT_IMAGES_DIR = '~/Pictures/'


def get_is_debug() -> bool:
    return os.getenv('ISEARCHD_DEBUB') is not None


def get_socket_path() -> str:
    return os.getenv('ISEARCHD_SOCKET') or os.path.expanduser(DEFAULT_SOCKET)


def get_db_path() -> str:
    return os.getenv('ISEARCHD_DB') or os.path.expanduser(DEFAULT_DB)


def get_default_watching_dir() -> str:
    env_path = os.getenv('ISEARCHD_IMAGES_DIR')
    if env_path:
        return os.path.expanduser(env_path)
    return os.path.expanduser(DEFAULT_IMAGES_DIR)
