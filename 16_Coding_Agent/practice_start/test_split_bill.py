import unittest

from split_bill import split_bill


class SplitBillTest(unittest.TestCase):
    def test_two_friends(self):
        self.assertEqual(split_bill(50, 2), 25)

    def test_three_friends(self):
        self.assertEqual(split_bill(60.30, 3), 20.10)
