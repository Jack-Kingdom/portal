from tornado import web


class ShortURLHandler(web.RequestHandler):

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def get(self):
        self.write("Hello, world")


class AliasHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def get(self):
        self.write("Hello, world")


def make_app():
    return web.Application([
        (r"/api/v1/shortURL", ShortURLHandler),
        (r"/api/v1/shortURL/([0-9a-zA-Z\-_.~]+)", ShortURLHandler),
        (r"/api/v1/alias", AliasHandler),
    ])
