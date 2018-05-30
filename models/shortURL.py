import logging
from meta import mapper
from meta.validator import Validator
from models.base import BaseModel
from models.template import shortURL_template

logger = logging.getLogger(__name__)


class ShortURLModel(BaseModel):
    def __init__(self):
        super(ShortURLModel, self).__init__(shortURL_template)

    def insert(self, dst: str):
        v = Validator()
        if not v.is_url_legal(dst):
            raise ValueError('dst url not illegal')

        logger.info('create shortURL for dst: {uri}'.format(uri=dst))

        with self.get_cursor() as cursor:
            # TODO: redesign this part
            # it's so bad here, do not hack in models

            for line in self.template['insert'].split('\n'):
                if '?' in line:
                    logger.debug('execute sql: {sql}, value: {value}'.format(sql=line, value=(dst,)))
                    cursor.execute(line, (dst,))
                else:
                    logger.debug('execute sql: {sql}'.format(sql=line))
                    cursor.execute(line)
                    if 'select'.upper() in line:
                        num, = cursor.fetchone()
            self.conn.commit()

        src = mapper.num2uri(int(num))

        if hasattr(self, 'cache'):
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
        with self.get_cursor() as cursor:
            cursor.execute(self.template['delete'], (num,))
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

        logger.info('update shortURL from src: {src_uri} to dst: {dst_uri}'.format(
            src_uri=src, dst_uri=dst))

        if not self.retrieve(src, use_cache=False):
            return False, 'shortURL src not exist.'

        num = mapper.uri2num(src)
        with self.get_cursor() as cursor:
            cursor.execute(self.template['update'], (dst, num))
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

        logger.info('retrieve shortURL from src: {uri}'.format(uri=src))

        num = mapper.uri2num(src)
        logger.debug('src: {src} map to num: {num}'.format(src=src, num=num))

        with self.get_cursor() as cursor:
            logger.debug('execute sql: {sql}, value: {value}'.format(
                sql=self.template['query'],
                value=(num,)))
            cursor.execute(self.template['query'], (num,))
            dst = cursor.fetchone()
            logger.debug('queried dst: {value}, type: {type}'.format(value=dst, type=type(dst)))
            dst = dst[0] if dst else None

        if hasattr(self, 'cache') and use_cache:
            self.cache.set(src, dst, expire=self.cache_expire)

        return dst
