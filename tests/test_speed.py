from time import perf_counter
import unittest

import cornflakes


class TestSpeed(unittest.TestCase):
    """Tests for eval_datetime."""

    def test_ini_load_speed(self):
        s = perf_counter()
        cornflakes.ini_load("tests/configs/default.ini")
        s -= perf_counter()

        self.assertTrue(s > -0.001)
