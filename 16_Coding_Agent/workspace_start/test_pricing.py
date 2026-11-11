import unittest

from pricing import apply_discount


class ApplyDiscountTest(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(apply_discount(0.99, 0), 0.99)

    def test_ten_percent_off_an_album(self):
        self.assertEqual(apply_discount(9.99, 10), 8.99)
