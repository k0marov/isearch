import sys
import di

if __name__ == '__main__':
    executor = di.Init()
    executor.execute(sys.argv[1:])
