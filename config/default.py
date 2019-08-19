"""
default config defined in this file
"""

default_config = {
    "DEBUG": int(False),

    "LISTENING_ADDRESS": "127.0.0.1",
    "LISTENING_PORT": "8888",

    "DB_HOST": "localhost",
    "DB_PORT": 3306,
    "DB_USER": "root",
    "DB_PASSWORD": "root",
    "DATABASE": "portal",

    "MEMCACHED_ADDRESS": "localhost",
    "MEMCACHED_PORT": 11211,
    "MEMCACHED_TIMEOUT": 1,

    "REDIRECT_STATUS_CODE": 302
}
