import logging
from meta.validator import Validator
from models.base import BaseModel
from models.template import alias_template

logger = logging.getLogger(__name__)


class AliasModel(BaseModel):
    def __init__(self):
        super(AliasModel, self).__init__(alias_template)

    def insert(self, dst: str):
        v = Validator()
        if not v.is_url_legal(dst):
            raise ValueError('dst url not illegal')

        with self.get_cursor() as cursor:
            cursor.execute(self.template['insert'], [dst])
            self.conn.commit()

    def delete(self, src: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')

        with self.get_cursor() as cursor:
            cursor.execute(self.template['delete'], [src])
            self.conn.commit()

    def update(self, src: str, dst: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')
        if not v.is_url_legal(dst):
            raise ValueError('dst url not illegal')

        with self.get_cursor() as cursor:
            cursor.execute(self.template['update'], [src, dst])
            self.conn.commit()

    def retrieve(self, src: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')

        with self.get_cursor() as cursor:
            cursor.execute(self.template['query'], [src])
            cursor.fetchall()
