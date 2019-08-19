"""
base model for shortURL and alias
wrapped some shared function here
"""

import pymysql
from config import CONFIG


class BaseModel(object):
    def __init__(self):

        self.conn = pymysql.connect(host=CONFIG['DB_HOST'],
                                    port=CONFIG['DB_PORT'],
                                    user=CONFIG['DB_USER'],
                                    password=CONFIG['DB_PASSWORD'],
                                    db=CONFIG['DATABASE'],
                                    charset='utf8mb4')

    def __del__(self):
        """
        close connection
        :return: None
        """
        self.conn.close()
