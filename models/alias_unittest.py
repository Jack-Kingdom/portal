import unittest
from models.alias import AliasModel
from utils.error import DestinationIllegal


class AliasModelUnitTest(unittest.TestCase):

    def setUp(self):
        self.m = AliasModel()

        with self.m.conn.cursor() as cursor:
            cursor.execute('DELETE FROM alias;')
            self.m.conn.commit()

        if hasattr(self.m, 'cache'):
            self.m.cache.flush_all()

    def tearDown(self):
        if hasattr(self.m, 'cache'):
            self.m.cache.close()

    def test_CURD(self):
        src = 'google'
        dst = 'https://google.com'
        changed_dst = 'https://youtube.com'

        self.assertTrue(self.m.insert(src, dst)[0])
        self.assertEqual(self.m.retrieve(src), dst)
        self.assertTrue(self.m.update(src, changed_dst)[0])
        self.assertEqual(self.m.retrieve(src), changed_dst)
        self.assertTrue(self.m.delete(src)[0])
        self.assertIsNone(self.m.retrieve(src))

    def test_insert_illegal(self):
        with self.assertRaises(DestinationIllegal):
            self.m.insert('google', '123')

    def test_duplicated_insert(self):
        src = 'google'
        dst = 'https://google.com'

        self.assertTrue(self.m.insert(src, dst)[0])
        self.assertFalse(self.m.insert(src, dst)[0])
