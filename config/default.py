"""
default config in this file
ODBC URI Scheme:
- https://tools.ietf.org/html/draft-patrick-lambert-odbc-uri-scheme-00
"""

default_config = {
    "DEBUG": False,

    "LISTENING_ADDRESS": "127.0.0.1",
    "LISTENING_PORT": "8888",

    "DB_HOST": "localhost",
    "DB_USER": "root",
    "DB_PASSWORD": "root",
    "DATABASE": "portal",

    "MEMCACHED_ADDRESS": "",
    "MEMCACHED_PORT": 11211,
    "MEMCACHED_TIMEOUT": 1,
    "MEMCACHED_CACHE_EXPIRE": 60 * 10,

    "REDIRECT_STATUS_CODE": 302
}
