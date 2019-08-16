from config import CONFIG
from pymemcache.client.base import Client

_memcached = None


def get_memcached_client():
    global _memcached
    if not _memcached:
        _memcached = Client((CONFIG['MEMCACHED_ADDRESS'], CONFIG['MEMCACHED_PORT']),
                            timeout=CONFIG['MEMCACHED_TIMEOUT'],
                            deserializer=lambda k, v, f: str(v, encoding='utf-8') if isinstance(v, bytes) else v)

    return _memcached
