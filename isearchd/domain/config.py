import dataclasses
import os

DEFAULT_SOCKET = '~/.cache/isearch/isearchd.sock'
DEFAULT_DB = '~/.cache/isearch/db.sqlite3'
DEFAULT_IMAGES_DIR = '~/Pictures/'

@dataclasses.dataclass
class Config:
    """Dataclass for config params."""
    socket_path: str
    db_path: str
    img_dir: str
    is_debug: bool
    is_integration_test: bool

def get_config_from_env() -> Config:
    return Config(
        socket_path=_get_socket_path(),
        db_path=_get_db_path(),
        img_dir=_get_default_watching_dir(),
        is_debug=_get_is_debug(),
        is_integration_test=_get_is_integration_test(),
    )

def _get_is_debug() -> bool:
    return os.getenv('ISEARCHD_DEBUB') != '0'

def _get_socket_path() -> str:
    return os.getenv('ISEARCHD_SOCKET') or os.path.expanduser(DEFAULT_SOCKET)


def _get_db_path() -> str:
    return os.getenv('ISEARCHD_DB') or os.path.expanduser(DEFAULT_DB)

def _get_default_watching_dir() -> str:
    env_path = os.getenv('ISEARCHD_IMAGES_DIR')
    if env_path:
        return os.path.expanduser(env_path)
    return os.path.expanduser(DEFAULT_IMAGES_DIR)

def _get_is_integration_test() -> bool:
    return os.getenv('ISEARCH_TEST') == '1'