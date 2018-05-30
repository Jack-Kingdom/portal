import logging
from meta.validator import Validator
from models.base import BaseModel
from models.template import alias_template

logger = logging.getLogger(__name__)


class AliasModel(BaseModel):
    def __init__(self):
        super(AliasModel, self).__init__()

        with self.conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS alias (
              src VARCHAR(255) PRIMARY KEY,
              dst VARCHAR(255) NOT NULL
            );""")
            self.conn.commit()

    def insert(self, src: str, dst: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            raise ValueError('src url can only contains unresolved char')
        if not v.is_url_legal(dst):
            raise ValueError('dst url not illegal')

        if self.retrieve(src, use_cache=False):
            return False, 'alias src has exists.'

        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO alias VALUES (%s ,%s);", (src, dst))
            self.conn.commit()

        if hasattr(self, 'cache'):
            self.cache.set(src, dst, expire=self.cache_expire)

        return True, None

    def delete(self, src: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')

        if not self.retrieve(src, use_cache=False):
            return False, 'alias src not exist.'

        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM alias WHERE src=%s;', (src,))
            self.conn.commit()

        if hasattr(self, 'cache'):
            self.cache.delete(src)

        return True, None

    def update(self, src: str, dst: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')
        if not v.is_url_legal(dst):
            raise ValueError('dst url not illegal')

        if not self.retrieve(src, use_cache=False):
            return False, 'alias src not exist.'

        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE alias SET dst=%s WHERE src=%s;", (dst, src))
            self.conn.commit()

        if hasattr(self, 'cache'):
            self.cache.set(src, dst, expire=self.cache_expire)

        return True, None

    def retrieve(self, src: str, use_cache=True):

        if hasattr(self, 'cache') and use_cache:
            dst = self.cache.get(src)
            if dst:
                return dst

        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')

        with self.conn.cursor() as cursor:
            cursor.execute('SELECT dst FROM alias WHERE src=%s;', (src,))
            result = cursor.fetchone()
            dst, = result if result else (None,)

        if hasattr(self, 'cache') and use_cache:
            self.cache.set(src, dst, expire=self.cache_expire)

        return dst
