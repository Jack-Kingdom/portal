import re
import unittest
from meta.char import url_unreserved_characters, url_unreserved_characters_length


class UnitTest(unittest.TestCase):

    def setUp(self):
        self.re_expr = re.compile(r'^[0-9a-zA-Z\-_.~]$')

    def test_contains(self):

        for i in range(128):
            c = chr(i)
            if self.re_expr.match(c):
                self.assertIn(c, url_unreserved_characters)
            else:
                self.assertNotIn(c, url_unreserved_characters)

    def test_length(self):

        should_length = 0
        for i in range(128):
            c = chr(i)
            if self.re_expr.match(c):
                should_length += 1

        self.assertEqual(should_length, url_unreserved_characters_length)


if __name__ == '__main__':
    unittest.main()
