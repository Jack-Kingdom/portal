"""
base model for shortURL and alias
wrapped some shared function here
"""

import os
from config import CONFIG


class Cursor(object):

    def __init__(self, conn):
        self.conn = conn
        self.cursor = None

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()


class BaseModel(object):
    def __init__(self, template):
        self.template = template

        if CONFIG['DATABASE_URI']:
            import pyodbc
            self.conn = pyodbc.connect(CONFIG['DATABASE_URI'])
        else:
            import sqlite3
            self.conn = sqlite3.connect(os.path.join(os.curdir, 'database.sqlite'))

        with self.get_cursor() as cursor:
            cursor.execute(template['init'])
            self.conn.commit()

        if CONFIG['MEMCACHED_ADDRESS'] and CONFIG['MEMCACHED_PORT']:
            from pymemcache.client.base import Client
            host, port = CONFIG['MEMCACHED_ADDRESS'], CONFIG['MEMCACHED_PORT']
            self.cache = Client((host, port),
                                timeout=CONFIG['MEMCACHED_TIMEOUT'],
                                deserializer=lambda k, v, f: str(v, encoding='utf-8') if isinstance(v, bytes) else v
                                )
            self.cache_expire = CONFIG['MEMCACHED_CACHE_EXPIRE']

    def __del__(self):
        if hasattr(set, 'cache'):
            self.cache.close()

        self.conn.close()

    def get_cursor(self):
        return Cursor(self.conn)
