from tornado import web
from config import CONFIG
from .shortURL import ShortURLHandler


def make_app():
    return web.Application([
        (r"^/api/v1/shortURL$", ShortURLHandler),
        (r"^/api/v1/shortURL/([0-9a-zA-Z\-_.~]+)$", ShortURLHandler),
    ], debug=CONFIG['DEBUG'])
