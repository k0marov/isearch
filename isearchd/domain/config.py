import dataclasses
import os


@dataclasses.dataclass
class Config:
    socket_path: str
    db_path: str

def get_socket_path() -> str:
    return os.getenv('ISEARCHD_SOCKET') or os.path.expanduser('~/.cache/isearch/isearchd.sock')

def get_db_path() -> str:
    return os.getenv('ISEARCHD_DB') or os.path.expanduser('~/.cache/isearch/db.sqlite3')

def get_default_watching_dir() -> str:
    return os.getenv('ISEARCHD_IMAGES_DIR') or os.path.expanduser('~/Pictures/')
