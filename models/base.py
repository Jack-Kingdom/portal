"""
base model for shortURL and alias
wrapped some shared function here
"""

import pymysql
from pymemcache.client.base import Client
from config import CONFIG


class BaseModel(object):
    def __init__(self):

        self.conn = pymysql.connect(host=CONFIG['DB_HOST'],
                                    user=CONFIG['DB_USER'],
                                    password=CONFIG['DB_PASSWORD'],
                                    db=CONFIG['DATABASE'],
                                    charset='utf8mb4')

        if CONFIG['MEMCACHED_ADDRESS'] and CONFIG['MEMCACHED_PORT']:
            host, port = CONFIG['MEMCACHED_ADDRESS'], CONFIG['MEMCACHED_PORT']
            self.cache = Client((host, port),
                                timeout=CONFIG['MEMCACHED_TIMEOUT'],
                                deserializer=lambda k, v, f: str(v, encoding='utf-8') if isinstance(v, bytes) else v)
            self.cache_expire = CONFIG['MEMCACHED_CACHE_EXPIRE']

    def __del__(self):
        if hasattr(set, 'cache'):
            self.cache.close()

        self.conn.close()
