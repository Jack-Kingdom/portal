"""
some mapper function declared in this file:
- num2uri: convert number to uri
- uri2num: convert a uri to number
"""

from meta.char import url_unreserved_characters, \
    url_unreserved_characters_length


def num2uri(num: int) -> str:
    result = ''
    while num:
        remainder = num % url_unreserved_characters_length
        result = url_unreserved_characters[remainder] + result
        num //= url_unreserved_characters_length
    return result


def uri2num(uri: str) -> int:
    result = 0
    for i, c in enumerate(uri[::-1]):
        if c not in url_unreserved_characters:
            raise ValueError('character {char} is not allowed in uri'.format(char=c))

        result += url_unreserved_characters.index(c) * (url_unreserved_characters_length ** i)
    return result


def next_uri(uri: str) -> str:
    return num2uri(uri2num(uri) + 1)
