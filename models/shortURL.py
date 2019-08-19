import logging
from meta import mapper
from models.base import BaseModel
from utils.error import CodeError
from utils.decr.cached import cached
from utils.cache import get_memcached_client
from utils.code import SourceURLNotExist

logger = logging.getLogger(__name__)


class ShortURLModel(BaseModel):

    def __init__(self):
        super(ShortURLModel, self).__init__()

        with self.conn.cursor() as cursor:
            cursor.execute("""
         CREATE TABLE IF NOT EXISTS shortURL ( 
          id  INTEGER PRIMARY KEY AUTO_INCREMENT, 
          dst VARCHAR(255) NOT NULL,
          status_code ENUM('301', '302') DEFAULT '301',
          permanent BOOL NOT NULL DEFAULT FALSE ,
          duration INTEGER NOT NULL DEFAULT 2592000,
          created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          modified_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          KEY adx_id (id)
        );""")
            self.conn.commit()

    def insert(self, dst: str):
        logger.info('create shortURL for dst: {uri}'.format(uri=dst))
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO shortURL VALUES (DEFAULT, %s, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT);", (dst,))
            num = cursor.lastrowid
            self.conn.commit()
        return mapper.num2uri(num)

    def delete(self, src: str):
        logger.info('delete shortURL for src: {uri}'.format(uri=src))

        num = mapper.uri2num(src)
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT dst FROM shortURL WHERE id=%s', (num,))
            result = cursor.fetchone()
            if not result:
                raise CodeError(SourceURLNotExist)

            cursor.execute('DELETE FROM shortURL WHERE id=%s', (num,))
            self.conn.commit()

        self.retrieve(src, clear=True)

    def update(self, src: str, dst: str):

        num = mapper.uri2num(src)
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT dst FROM shortURL WHERE id=%s', (num,))
            result = cursor.fetchone()
            if not result:
                raise CodeError(SourceURLNotExist)

            cursor.execute('UPDATE shortURL SET dst=%s WHERE id=%s;', (dst, num))
            self.conn.commit()

        self.retrieve(src, rewrite=True)  # update cache

    @cached(lambda obj, src: src, clients=(get_memcached_client(),), prefix='portal')
    def retrieve(self, src: str, *args, **kwargs):
        num = mapper.uri2num(src)
        logger.debug('src: {src} map to num: {num}'.format(src=src, num=num))
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT dst FROM shortURL WHERE id=%s', (num,))
            result = cursor.fetchone()

            if not result:
                raise CodeError(SourceURLNotExist)

            return result[0]
