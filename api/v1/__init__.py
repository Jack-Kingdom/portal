from tornado import web
from config import CONFIG
from .shortURL import ShortURLHandler
from .alias import AliasHandler


def make_app():
    return web.Application([
        (r"^/api/v1/shortURL$", ShortURLHandler),
        (r"^/api/v1/shortURL/([0-9a-zA-Z\-_.~]+)$", ShortURLHandler),
        (r"/api/v1/alias", AliasHandler),
        (r"/api/v1/alias/([0-9a-zA-Z\-_.~]+)", AliasHandler),
    ], debug=CONFIG['DEBUG'])
