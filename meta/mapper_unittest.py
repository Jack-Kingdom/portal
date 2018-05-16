import random
import unittest
from meta.mapper import uri2num, num2uri


class MapperUnitTest(unittest.TestCase):

    def test_equivalence(self):
        random_num = random.randint(64 ** 3, 64 ** 5)
        converted_uri = num2uri(random_num)
        restored_num = uri2num(converted_uri)
        self.assertEqual(random_num, restored_num)


if __name__ == '__main__':
    unittest.main()
