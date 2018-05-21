"""
base model for shortURL and alias
wrapped some shared function here
"""

import pyodbc
from config import CONFIG


class BaseModel(object):
    def __init__(self, template):
        self.template = template

        self.conn = pyodbc.connect(CONFIG['DATABASE_URI'])
        self.cursor = self.conn.cursor()

        self.cursor.execute(template['init'])
        self.cursor.commit()
