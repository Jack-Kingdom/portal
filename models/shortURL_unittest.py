import unittest
from models.shortURL import ShortURLModel


class ShortURLModelUnitTest(unittest.TestCase):

    def setUp(self):
        self.m = ShortURLModel()

        with self.m.get_cursor() as cursor:
            cursor.execute('DELETE FROM shortURL;')
            self.m.conn.commit()

        if hasattr(self.m, 'cache'):
            self.m.cache.flush_all()

    def tearDown(self):
        if hasattr(self.m, 'cache'):
            self.m.cache.close()

    def test_CURD(self):
        dst = 'https://google.com'
        changed_dst = 'https://youtube.com'
        _, src = self.m.insert(dst)

        self.assertIsNotNone(src)
        self.assertTrue(self.m.update(src, changed_dst)[0])
        self.assertEqual(self.m.retrieve(src), changed_dst)
        self.assertTrue(self.m.delete(src))
        self.assertIsNone(self.m.retrieve(src))

    def test_insert_illegal(self):
        with self.assertRaises(ValueError):
            self.m.insert('123')
