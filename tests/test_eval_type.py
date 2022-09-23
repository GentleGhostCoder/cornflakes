import sys
import unittest
from datetime import datetime, timedelta, timezone
from ipaddress import ip_address

import cornflakes


class TestEvalType(unittest.TestCase):
    """Tests for eval_type."""

    def test_none(self):
        [self.assertEqual(cornflakes.eval_type(str(x)), None) for x in ["''", '""', ""]]

    def test_dot(self):
        self.assertEqual(cornflakes.eval_type("'.'"), ".")

    def test_integer(self):
        [self.assertEqual(cornflakes.eval_type(str(x)), x) for x in [*range(10), sys.maxsize, -sys.maxsize]]

    def test_float(self):
        [self.assertEqual(cornflakes.eval_type(str(x)), x) for x in [0.1, 1.0, 0.0, -0.1, 0.00000000000000000012312301]]

    def test_ipv4(self):
        [self.assertEqual(cornflakes.eval_type(x), ip_address(x)) for x in ["1.1.1.1", "1:1:1:1:1:1:1:1"]]
        # wrong
        [
            self.assertEqual(cornflakes.eval_type(x), x)
            for x in [
                "1.1.1.01",
                "1:1:1:1:1:1:1:x",
                "0.0.0.256",
                "::1",
                ":::::::",
                "...",
            ]
        ]

    def test_timestamp_formats(self):
        [
            self.assertTrue(type(cornflakes.eval_type(str(x))) in [datetime, cornflakes.DatetimeMS])
            for x in [
                "20060317 13:27:54.123",
                "2006/03/17 13:27:54.123",
                "17/03/2006 13:27:54.123",
                "20060317 13:27:54",
                "2006/03/17 13:27:54",
                "17/03/2006 13:27:54",
                "2006-03-17 13:27:54.123",
                "17-03-2006 13:27:54.123",
                "2006-03-17 13:27:54",
                "17-03-2006 13:27:54",
                "2006-03-17T13:27:54",
                "2006-03-17T13:27:54.123",
                "20060317T13:27:54",
                "20060317T13:27:54.123",
                "17-03-2006T13:27:54.123",
                "17-03-2006T13:27:54",
                "2006-03-17T13:27:54Z",
                "2006-03-17T13:27:54+03:45",
                "2006-03-17T13:27:54-05:37",
                "2006-03-17T13:27Z",
                "2006-03-17T13:27+03:45",
                "2006-03-17T13:27-05:37",
                "17/Mar/2006:13:27:54 -0537",
                "17/Mar/2006:13:27:54 +0537",
                "Sat, 17 Mar 2006 13:27:54 GMT",
                "Sat, 17 Mar 2006 13:27:54 EST",
                "Sat, 17 Mar 2006 13:27:54 UT",
                "Sat, 17 Mar 2006 13:27:54 M",
                "Sat, 17 Mar 2006 13:27:54 -0234",
                "Sat, 17 Mar 2006 13:27:54 +0325",
            ]
        ]

    def test_timestamp_values(self):
        self.assertEqual(
            str(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 +0325")),
            "2006-03-17 13:27:54+03:25",
        )
        self.assertEqual(str(cornflakes.eval_type("20060317 13:27:54.123")), "2006-03-17 13:27:54.123000+00")
        self.assertEqual(str(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 EST")), "2006-03-17 13:27:54-05:00")
        self.assertEqual(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").year, 2006)
        self.assertEqual(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").day, 17)
        self.assertEqual(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").month, 3)
        self.assertEqual(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").hour, 13)
        self.assertEqual(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").minute, 27)
        self.assertEqual(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").second, 54)
        self.assertEqual(cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").microsecond, 0)
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        self.assertEqual(days[cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").isoweekday()], "Saturday")
        self.assertEqual(
            cornflakes.eval_type("Sat, 17 Mar 2006 13:27:54 -0234").tzinfo,
            timezone(timedelta(-1, 77160)),
        )

    def test_wrong_timestamp_values(self):
        self.assertEqual(
            cornflakes.eval_type("2017-01-01 24:23:23"),
            "2017-01-01 24:23:23",
        )
