import tornado.ioloop
import tornado.web


class ShortURLHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def get(self):
        self.write("Hello, world")


class AliasHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/api/v1/shortURL", ShortURLHandler),
        (r"/api/v1/alias", AliasHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
