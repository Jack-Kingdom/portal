import logging
from meta import mapper
from meta.validator import Validator
from models.base import BaseModel
from models.template import shortURL_template

logger = logging.getLogger(__name__)


class ShortURLModel(BaseModel):

    def __init__(self):
        super(ShortURLModel, self).__init__()

        with self.conn.cursor() as cursor:
            cursor.execute("""
         CREATE TABLE IF NOT EXISTS shortURL ( 
          id  INTEGER PRIMARY KEY AUTO_INCREMENT, 
          dst VARCHAR(255) NOT NULL 
        );""")
            self.conn.commit()

    def insert(self, dst: str):
        v = Validator()
        if not v.is_url_legal(dst):
            raise ValueError('dst url not illegal')

        logger.info('create shortURL for dst: {uri}'.format(uri=dst))

        with self.conn.cursor() as cursor:
            cursor.execute("START TRANSACTION;")
            cursor.execute("INSERT INTO shortURL VALUES (NULL ,%s);", (dst,))
            cursor.execute("SELECT id FROM shortURL ORDER BY id DESC LIMIT 1;")
            result = cursor.fetchone()
            num, = result if result else (None,)
            cursor.execute("COMMIT;")
            self.conn.commit()

        src = mapper.num2uri(int(num))

        if hasattr(self, 'cache'):
            logger.info('cached set: src:{},dst:{}'.format(src, dst))
            self.cache.set(src, dst, expire=self.cache_expire)

        return True, src

    def delete(self, src: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')

        logger.info('delete shortURL for src: {uri}'.format(uri=src))

        if not self.retrieve(src, use_cache=False):
            return False, 'shortURL src not exist.'

        num = mapper.uri2num(src)
        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM shortURL WHERE id=%s', (num,))
            self.conn.commit()

        if hasattr(self, 'cache'):
            logger.info('cached delete: src:{}'.format(src))
            self.cache.delete(src)

        return True, None

    def update(self, src: str, dst: str):
        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')
        if not v.is_url_legal(dst):
            raise ValueError('dst url not illegal')

        logger.info('update shortURL from src: {src_uri} to dst: {dst_uri}'.format(
            src_uri=src, dst_uri=dst))

        if not self.retrieve(src, use_cache=False):
            return False, 'shortURL src not exist.'

        num = mapper.uri2num(src)
        with self.conn.cursor() as cursor:
            cursor.execute('UPDATE shortURL SET dst=%s WHERE id=%s;', (dst, num))
            self.conn.commit()

        if hasattr(self, 'cache'):
            logger.info('cached set: src:{},dst:{}'.format(src, dst))
            self.cache.set(src, dst, expire=self.cache_expire)

        return True, None

    def retrieve(self, src: str, use_cache=True):

        if hasattr(self, 'cache') and use_cache:
            dst = self.cache.get(src)
            if dst:
                logger.info('cached hit: src:{},dst:{}'.format(src, dst))
                return dst
            else:
                logger.info('cached missed: src:{}'.format(src))

        v = Validator()
        if not v.is_contains_unresolved_char_only(src):
            return ValueError('src url can only contains unresolved char')

        logger.info('retrieve shortURL from src: {uri}'.format(uri=src))

        num = mapper.uri2num(src)
        logger.debug('src: {src} map to num: {num}'.format(src=src, num=num))

        with self.conn.cursor() as cursor:
            cursor.execute('SELECT dst FROM shortURL WHERE id=%s', (num,))
            result = cursor.fetchone()
            dst, = result if result else (None,)

        if hasattr(self, 'cache') and use_cache and dst:
            logger.info('cached set: src:{},dst:{}'.format(src, dst))
            self.cache.set(src, dst, expire=self.cache_expire)

        return dst
