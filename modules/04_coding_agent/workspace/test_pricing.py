import unittest
from pricing import apply_discount


class PricingTest(unittest.TestCase):
    def test_ten_percent_off_100(self):
        self.assertEqual(apply_discount(100, 10), 90)
