import pickle
from config import CONFIG
from pymemcache.client.base import Client

_memcached = None


def get_memcached_client():
    global _memcached
    if not _memcached:
        _memcached = Client((CONFIG['MEMCACHED_ADDRESS'], CONFIG['MEMCACHED_PORT']),
                            timeout=CONFIG['MEMCACHED_TIMEOUT'],
                            serializer=lambda k, v: (pickle.dumps(v), 0),
                            deserializer=lambda k, v, f: pickle.loads(v))
    return _memcached
