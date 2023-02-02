import os
from time import perf_counter
import unittest

import pytest

import cornflakes


class TestSpeed(unittest.TestCase):
    """Tests for eval_datetime."""

    @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
    def test_ini_load_speed(self):
        s = perf_counter()
        for _ in range(1000):
            cornflakes.ini_load("tests/configs/default.ini")
        self.assertTrue(0.11 > (perf_counter() - s))

    @pytest.mark.skipif(os.environ.get("NOX_RUNNING", "False"))
    def test_eval_csv_speed(self):
        s = perf_counter()
        with open("tests/smallwikipedia.csv", "rb") as f:
            data = f.read(10000)
            for _ in range(1000):
                cornflakes.eval_csv(data)
        self.assertTrue(0.15 > (perf_counter() - s))
