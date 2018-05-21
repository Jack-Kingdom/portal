"""
default config in this file
ODBC URI Scheme:
- https://tools.ietf.org/html/draft-patrick-lambert-odbc-uri-scheme-00
"""

default_config = {
    "DEBUG": False,

    "LISTENING_ADDRESS": "127.0.0.1",
    "LISTENING_PORT": "8888",

    "DATABASE_URI": "",

    "ENABLE_MEMCACHED": False,
    "MEMCACHED_URI": "localhost:11211",

    "REDIRECT_STATUS_CODE": 302
}
