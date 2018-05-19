"""
this file supplied some function that \
used to check url is illegal or not.
"""

import re
from utils import decr


@decr.SingletonDecorator
class Validator(object):
    def __init__(self):
        self.unresolved_char_re = re.compile(r'[0-9a-zA-Z\-_.~]+')

    def contains_unresolved_char_only(self, url):
        return bool(self.unresolved_char_re.fullmatch(url))

    def is_url_legal(self, url):
        pass
        # todo add url legal check here
