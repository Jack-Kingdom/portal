"""
base model for shortURL and alias
wrapped some shared function here
"""

import os
from config import CONFIG


class Cursor(object):

    def __init__(self, conn):
        self.conn = conn
        self.cursor = None

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()


class BaseModel(object):
    def __init__(self, template):
        self.template = template

        if CONFIG['DATABASE_URI']:
            pyodbc = __import__('pyodbc')
            self.conn = pyodbc.connect(CONFIG['DATABASE_URI'])
        else:
            sqlite3 = __import__('sqlite3')
            self.conn = sqlite3.connect(os.path.join(os.curdir, 'database.sqlite'))

        with self.get_cursor() as cursor:
            cursor.execute(template['init'])

    def __del__(self):
        self.conn.close()

    def get_cursor(self):
        return Cursor(self.conn)
