import unittest
from totals import line_total


class TotalsTest(unittest.TestCase):
    def test_two_at_ten(self):
        self.assertEqual(line_total(2, 10), 20)
