from tornado import web, escape
from config import CONFIG
from meta.validator import Validator
from models import ShortURLModel


class ShortURLHandler(web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(ShortURLHandler, self).__init__(application, request, **kwargs)

        self.model = ShortURLModel()

    def post(self, *args):
        if args:
            raise web.HTTPError(404)

        data = escape.json_decode(self.request.body)
        if 'dst' not in data:
            raise web.HTTPError(400, 'dst url must be supplied.')

        dst = data['dst']

        v = Validator()
        if not v.is_url_legal(dst):
            raise web.HTTPError(400, 'dst url illegal.')

        src = self.model.insert(data['dst'])

        self.write(escape.json_encode({'src': src, 'dst': dst}))

    def delete(self, src):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            self.set_status(400)
            raise web.HTTPError(400, 'src url can only contains unresolved char.')

        self.model.delete(src)

    def put(self, src):
        data = escape.json_decode(self.request.body)
        if 'dst' not in data:
            raise web.HTTPError(400, 'dst url must be supplied.')

        dst = data['dst']
        v = Validator()
        if not v.is_url_legal(dst):
            raise web.HTTPError(400, 'dst url illegal.')

        self.model.update(src, dst)

    def get(self, src):
        dst = self.model.retrieve(src)
        if dst:
            self.redirect(dst, status=CONFIG['REDIRECT_STATUS_CODE'])
        else:
            raise web.HTTPError(404)


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
        (r"^/api/v1/shortURL$", ShortURLHandler),
        (r"^/api/v1/shortURL/([0-9a-zA-Z\-_.~]+)$", ShortURLHandler),
        (r"/api/v1/alias", AliasHandler),
        (r"/api/v1/alias/([0-9a-zA-Z\-_.~]+)", AliasHandler),
    ], debug=CONFIG['DEBUG'])
