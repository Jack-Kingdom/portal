"""
this file implemented a Validator class \
used to check url is legal or not.
"""

import re
from utils.decr.singleton import SingletonDecorator

unresolved_char_re = re.compile(r'[0-9a-zA-Z\-_.~]+')
url_legal_re = re.compile(r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")


@SingletonDecorator
class Validator(object):

    @staticmethod
    def is_contains_unresolved_char_only(url):
        return bool(unresolved_char_re.fullmatch(url))

    @staticmethod
    def is_url_legal(url):
        return bool(url_legal_re.fullmatch(url))
