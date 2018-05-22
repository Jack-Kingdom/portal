import unittest
from models.shortURL import ShortURLModel


class ShortURLModelUnitTest(unittest.TestCase):

    def setUp(self):
        self.m = ShortURLModel()

    def test_insert(self):
        src = self.m.insert('https://google.com')
        self.assertIsInstance(src, str)

        self.m.delete(src)

    def test_insert_illegal(self):
        with self.assertRaises(ValueError):
            self.m.insert('123')

    def test_delete(self):
        src = self.m.insert('https://google.com')

        self.assertIsNotNone(self.m.retrieve(src))
        self.m.delete(src)
        self.assertIsNone(self.m.retrieve(src))

    def test_update(self):
        dst = 'https://google.com'
        changed_dst = 'https://youtube.com'
        src = self.m.insert(dst)

        self.assertEqual(self.m.retrieve(src), dst)
        self.m.update(src, changed_dst)
        self.assertEqual(self.m.retrieve(src), changed_dst)

        self.m.delete(src)

    def test_retrieve(self):
        dst = 'https://google.com'
        src = self.m.insert(dst)

        self.assertEqual(self.m.retrieve(src), dst)
        self.m.delete(src)
        self.assertIsNone(self.m.retrieve(src))


if __name__ == '__main__':
    unittest.main()
