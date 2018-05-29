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

        suc, src = self.model.insert(data['dst'])

        if suc:
            self.write(escape.json_encode({'src': src, 'dst': dst}))
        else:
            err = src
            raise web.HTTPError(400, err)

    def delete(self, src=None):
        if not src:
            raise web.HTTPError(404)

        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            self.set_status(400)
            raise web.HTTPError(400, 'src url can only contains unresolved char.')

        suc, err = self.model.delete(src)
        if not suc:
            raise web.HTTPError(400, err)

    def put(self, src=None):
        if not src:
            raise web.HTTPError(404)

        data = escape.json_decode(self.request.body)
        if 'dst' not in data:
            raise web.HTTPError(400, 'dst url must be supplied.')
        dst = data['dst']

        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            raise web.HTTPError(400, 'src url can only contains unresolved char.')
        if not v.is_url_legal(dst):
            raise web.HTTPError(400, 'dst url illegal.')

        suc, err = self.model.update(src, dst)
        if not suc:
            raise web.HTTPError(400, err)

    def get(self, src=None):
        if not src:
            raise web.HTTPError(404)

        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            if CONFIG['DEBUG']:
                raise web.HTTPError(400, 'src url can only contains unresolved char.')
            else:
                raise web.HTTPError(404)

        dst = self.model.retrieve(src)
        if dst:
            self.redirect(dst, status=CONFIG['REDIRECT_STATUS_CODE'])
        else:
            raise web.HTTPError(404)
