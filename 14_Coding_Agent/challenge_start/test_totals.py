import unittest

from totals import line_total


class LineTotalTest(unittest.TestCase):
    def test_one_track(self):
        self.assertEqual(line_total(1.99, 1), 1.99)

    def test_two_tracks(self):
        self.assertEqual(line_total(0.99, 2), 1.98)
