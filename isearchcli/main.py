import sys
import di
from domain import config

if __name__ == '__main__':
    cfg = config.Config(socket_path=config.get_socket_path())
    executor = di.Init(cfg)
    executor.execute(sys.argv[1:])