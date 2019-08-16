import functools
from tornado import web, escape
from config import CONFIG
from meta.validator import Validator
from models.shortURL import ShortURLModel


def validate_src(func):
    @functools.wraps(func)
    def wrapper(obj, src, *args, **kwargs):
        if not src:
            raise web.HTTPError(404)
        if Validator.is_contains_unresolved_char_only(src):
            raise web.HTTPError(400, 'src url can only contains unresolved char.')

        return func(obj, src, *args, **kwargs)

    return wrapper


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

        suc, src = self.model.insert(data['dst'])

        if suc:
            self.write(escape.json_encode({'src': src, 'dst': dst}))
        else:
            err = src
            raise web.HTTPError(400, err)

    @validate_src
    def delete(self, src=None):
        suc, err = self.model.delete(src)
        if not suc:
            raise web.HTTPError(400, err)

    @validate_src
    def put(self, src=None):

        data = escape.json_decode(self.request.body)
        if 'dst' not in data:
            raise web.HTTPError(400, 'dst url must be supplied.')
        dst = data['dst']

        if not Validator.is_url_legal(dst):
            raise web.HTTPError(400, 'dst url illegal.')

        suc, err = self.model.update(src, dst)
        if not suc:
            raise web.HTTPError(400, err)

    @validate_src
    def get(self, src=None):

        dst = self.model.retrieve(src)
        if dst:
            self.redirect(dst, status=CONFIG['REDIRECT_STATUS_CODE'])
        else:
            raise web.HTTPError(404)
