"""
this file defined a decorator, used to cached func result
"""

import random
import functools

DEFAULT_TIMEOUT = 600
DEFAULT_RATIO = 0.25
DEFAULT_FACTOR = 1.5


def cached(to_key, clients, prefix=None,
           timeout=DEFAULT_TIMEOUT, ratio=DEFAULT_RATIO, factor=DEFAULT_FACTOR):
    """
    cache current function's result
    :param to_key: a str or a func that returned a cached key
    :param clients: cache clients
    :param prefix: prefix string for key, used to avoid collision
    :param timeout: cache last duration, unit: seconds
    :param ratio: a float number lower than 1, used to avoid cache avalanche
                current cache layer's timeout equal to current_timeout * random.uniform(1-n, 1+n)
    :param factor: timeout factor for next cache layer,
                next cache layer's timeout equal to current_timeout * (1 + factor)
    :return original wrapped function's result
    """

    assert isinstance(clients, tuple)  # clients must iterable

    def wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            key = to_key(*args, **kwargs) if callable(to_key) else str(to_key)
            key = (prefix + key) if prefix else key

            if not clients:
                return func(*args, **kwargs)

            client = clients[0]
            rst = client.get(key)
            if not rst:
                t = int(timeout * random.uniform(1 - ratio, 1 + ratio))
                rst = cached(to_key=key, clients=clients[1:], prefix=None,
                             timeout=int(t * factor), ratio=ratio, factor=factor)(func)(*args, **kwargs)
                client.set(key, rst, t)
            return rst

        return inner_wrapper

    return wrapper
