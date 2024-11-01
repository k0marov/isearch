HELP_MSG = \
    '''Usage: isearchd [OPTIONS] 
Daemon for the isearch system.

Options:
    -h, --help             show this help
    no options             start daemon

Environment variables:
    ISEARCHD_IMAGES_DIR     full path to directory which will be watched and indexed in realtime. Defaults to ~/Pictures
    ISEARCHD_SOCKET full    path to Unix socket where isearchd will serve requests. Defaults to ~/.cache/isearch/isearchd.sock
    ISEARCHD_DB             full path to SQLite db file. Defaults to ~/.cache/isearch/db.sqlite3
    ISEARCHD_DEBUG          set to 0 to disable debug. Defaults to True.
'''
