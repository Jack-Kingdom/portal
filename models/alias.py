import logging
from utils import error
from meta.validator import Validator
from models.base import BaseModel

logger = logging.getLogger(__name__)


class AliasModel(BaseModel):
    def __init__(self):
        super(AliasModel, self).__init__()

        with self.conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS alias (
              src VARCHAR(255) PRIMARY KEY,
              dst VARCHAR(255) NOT NULL,
              status_code ENUM('301', '302') DEFAULT '301',
              permanent BOOL NOT NULL DEFAULT FALSE ,
              duration INTEGER NOT NULL DEFAULT 2592000 ,
              created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
              modified_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              KEY idx_src (src)
            );""")
            self.conn.commit()

    def insert(self, src: str, dst: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            raise error.SourceIllegal('src url can only contains unresolved char')
        if not v.is_url_legal(dst):
            raise error.DestinationIllegal('dst url not illegal')

        if self.retrieve(src, with_cache=False):
            return False, 'alias src has exists.'

        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO alias VALUES (%s, %s, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT);", (src, dst))
            self.conn.commit()

        if hasattr(self, 'cache'):
            logger.info('cached set: src:{},dst:{}'.format(src, dst))
            self.cache.set(src, dst, expire=self.cache_expire)

        return True, None

    def delete(self, src: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return error.SourceIllegal('src url can only contains unresolved char')

        if not self.retrieve(src, with_cache=False):
            return False, 'alias src not exist.'

        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM alias WHERE src=%s;', (src,))
            self.conn.commit()

        if hasattr(self, 'cache'):
            logger.info('cached delete: src:{}'.format(src))
            self.cache.delete(src)

        return True, None

    def update(self, src: str, dst: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return error.SourceIllegal('src url can only contains unresolved char')
        if not v.is_url_legal(dst):
            raise error.DestinationIllegal('dst url not illegal')

        if not self.retrieve(src, with_cache=False):
            return False, 'alias src not exist.'

        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE alias SET dst=%s WHERE src=%s;", (dst, src))
            self.conn.commit()

        if hasattr(self, 'cache'):
            logger.info('cached set: src:{},dst:{}'.format(src, dst))
            self.cache.set(src, dst, expire=self.cache_expire)

        return True, None

    def retrieve(self, src: str, with_cache=True):

        if hasattr(self, 'cache') and with_cache:
            dst = self.cache.get(src)
            if dst:
                logger.info('cached hit: src:{},dst:{}'.format(src, dst))
                return dst
            else:
                logger.info('cached missed: src:{}'.format(src))

        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return error.SourceIllegal('src url can only contains unresolved char')

        with self.conn.cursor() as cursor:
            cursor.execute('SELECT dst FROM alias WHERE src=%s;', (src,))
            result = cursor.fetchone()
            dst, = result if result else (None,)

        if hasattr(self, 'cache') and with_cache and dst:
            logger.info('cached set: src:{},dst:{}'.format(src, dst))
            self.cache.set(src, dst, expire=self.cache_expire)

        return dst
