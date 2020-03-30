import unittest


class MyTestClass(unittest.TestCase):
    def test_my_method(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertTrue('FOO'.isupper())


if __name__ == '__main__':
    unittest.main()
