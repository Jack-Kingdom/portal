"""
this file implemented a Validator class \
used to check url is legal or not.
"""

import re
from utils import decr


@decr.SingletonDecorator
class Validator(object):
    def __init__(self):
        self.unresolved_char_re = re.compile(r'[0-9a-zA-Z\-_.~]+')
        self.url_legal_re = re.compile(
            r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")

    def is_contains_unresolved_char_only(self, url):
        return bool(self.unresolved_char_re.fullmatch(url))

    def is_url_legal(self, url):
        return bool(self.url_legal_re.fullmatch(url))
