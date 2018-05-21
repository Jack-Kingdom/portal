import random
import unittest
from meta.validator import Validator


class ValidatorUnitTest(unittest.TestCase):

    def test_unresolved_char(self):
        v = Validator()

        self.assertTrue(v.is_contains_unresolved_char_only('HelloWorld'))
        self.assertTrue(v.is_contains_unresolved_char_only('hello-world'))
        self.assertTrue(v.is_contains_unresolved_char_only('hello_world'))

        self.assertFalse(v.is_contains_unresolved_char_only('hello world'))
        self.assertFalse(v.is_contains_unresolved_char_only('hello_world!'))
        self.assertFalse(v.is_contains_unresolved_char_only('hello_world?'))

    def test_url_legal(self):
        v = Validator()

        self.assertTrue(v.is_url_legal('example.org'))
        self.assertTrue(v.is_url_legal('example.org:8000'))
        self.assertTrue(v.is_url_legal('http://example.org'))
        self.assertTrue(v.is_url_legal('https://example.org'))
        self.assertTrue(v.is_url_legal('https://example.org?arg=123'))
        self.assertTrue(v.is_url_legal('https://example.org?arg1=123&arg2=321'))

        self.assertFalse(v.is_url_legal('123'))
        self.assertFalse(v.is_url_legal('http:example.org'))


if __name__ == '__main__':
    unittest.main()
