from tornado import web, escape
from config import CONFIG
from meta.validator import Validator
from models import AliasModel


class AliasHandler(web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(AliasHandler, self).__init__(application, request, **kwargs)

        self.model = AliasModel()

    def post(self, *args):
        if args:
            raise web.HTTPError(404)

        data = escape.json_decode(self.request.body)
        if 'src' not in data or 'dst' not in data:
            raise web.HTTPError(400, 'src and dst url must be supplied.')
        src = data['src']
        dst = data['dst']

        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            raise web.HTTPError(400, 'src url can only contains unresolved char.')
        if not v.is_url_legal(dst):
            raise web.HTTPError(400, 'dst url illegal.')

        suc, err = self.model.insert(src, dst)

        if suc:
            self.write(escape.json_encode({'src': src, 'dst': dst}))
        else:
            raise web.HTTPError(400, err)

    def delete(self, src):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            self.set_status(400)
            raise web.HTTPError(400, 'src url can only contains unresolved char.')

        suc, err = self.model.delete(src)
        if not suc:
            raise web.HTTPError(400, err)

    def put(self, src):
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

    def get(self, src):

        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            raise web.HTTPError(400, 'src url can only contains unresolved char.')

        dst = self.model.retrieve(src)
        if dst:
            self.redirect(dst, status=CONFIG['REDIRECT_STATUS_CODE'])
        else:
            raise web.HTTPError(404)
