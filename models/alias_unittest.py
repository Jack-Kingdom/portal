import unittest
from models.alias import AliasModel


class AliasModelUnitTest(unittest.TestCase):

    def setUp(self):
        self.m = AliasModel()

    def test_insert(self):
        src = 'google'
        dst = 'https://google.com'
        self.m.insert(src, dst)

        self.assertEqual(dst, self.m.retrieve(src))

        self.m.delete(src)

    def test_insert_illegal(self):
        with self.assertRaises(ValueError):
            self.m.insert('google', '123')

    def test_duplicated_insert(self):
        pass

    def test_delete(self):
        src = 'google'
        dst = 'https://google.com'
        self.m.insert(src, dst)

        self.assertIsNotNone(self.m.retrieve(src))
        self.m.delete(src)
        self.assertIsNone(self.m.retrieve(src))

    def test_update(self):
        src = 'google'
        dst = 'https://google.com'
        changed_dst = 'https://youtube.com'
        self.m.insert(src, dst)

        self.assertEqual(self.m.retrieve(src), dst)
        self.m.update(src, changed_dst)
        self.assertEqual(self.m.retrieve(src), changed_dst)

        self.m.delete(src)

    def test_retrieve(self):
        src = 'google'
        dst = 'https://google.com'
        self.m.insert(src, dst)

        self.assertEqual(self.m.retrieve(src), dst)
        self.m.delete(src)
        self.assertIsNone(self.m.retrieve(src))
