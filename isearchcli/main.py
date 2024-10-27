import sys
import di
from domain import config

if __name__ == '__main__':
    cfg = config.Config("~/.cache/isearch/isearchd.sock")
    executor = di.Init(cfg)
    executor.execute(sys.argv[1:])