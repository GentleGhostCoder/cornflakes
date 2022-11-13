import datetime
import unittest

import cornflakes


class TestEvalDatetime(unittest.TestCase):
    """Tests for eval_datetime."""

    def test_timestamp_formats(self):
        [
            self.assertEqual(cornflakes.eval_datetime(string), value)
            for string, value in {
                "20060317 13:27:54.123": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, 123000, tzinfo=datetime.timezone.utc
                ),
                "2006/03/17 13:27:54.123": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, 123000, tzinfo=datetime.timezone.utc
                ),
                "17/03/2006 13:27:54.123": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, 123000, tzinfo=datetime.timezone.utc
                ),
                "20060317 13:27:54": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "2006/03/17 13:27:54": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "17/03/2006 13:27:54": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "2006-03-17 13:27:54.123": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, 123000, tzinfo=datetime.timezone.utc
                ),
                "17-03-2006 13:27:54.123": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, 123000, tzinfo=datetime.timezone.utc
                ),
                "2006-03-17 13:27:54": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "17-03-2006 13:27:54": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "2006-03-17T13:27:54": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "2006-03-17T13:27:54.123": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, 123000, tzinfo=datetime.timezone.utc
                ),
                "20060317T13:27:54": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "20060317T13:27:54.123": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, 123000, tzinfo=datetime.timezone.utc
                ),
                "17-03-2006T13:27:54.123": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, 123000, tzinfo=datetime.timezone.utc
                ),
                "17-03-2006T13:27:54": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "2006-03-17T13:27:54Z": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                "2006-03-17T13:27:54+03:45": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone(datetime.timedelta(seconds=13500))
                ),
                "2006-03-17T13:27:54-05:37": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=66180))
                ),
                "2006-03-17T13:27Z": datetime.datetime(2006, 3, 17, 13, 27, tzinfo=datetime.timezone.utc),
                "2006-03-17T13:27+03:45": datetime.datetime(
                    2006, 3, 17, 13, 27, tzinfo=datetime.timezone(datetime.timedelta(seconds=13500))
                ),
                "2006-03-17T13:27-05:37": datetime.datetime(
                    2006, 3, 17, 13, 27, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=66180))
                ),
                "17/Mar/2006:13:27:54 -0537": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=66180))
                ),
                "17/Mar/2006:13:27:54 +0537": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone(datetime.timedelta(seconds=20220))
                ),
                "Sat, 17 Mar 2006 13:27:54 GMT": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc
                ),
                "Sat, 17 Mar 2006 13:27:54 EST": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))
                ),
                "Sat, 17 Mar 2006 13:27:54 UT": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc
                ),
                "Sat, 17 Mar 2006 13:27:54 M": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=43200))
                ),
                "Sat, 17 Mar 2006 13:27:54 -0234": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=77160))
                ),
                "Sat, 17 Mar 2006 13:27:54 +0325": datetime.datetime(
                    2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone(datetime.timedelta(seconds=12300))
                ),
                "20060317": datetime.date(2006, 3, 17),
                "20061703": datetime.date(2006, 3, 17),
                "13:27:54.123": datetime.time(13, 27, 54, 123000, tzinfo=datetime.timezone.utc),
                "13:27:54": datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
            }.items()
        ]

        [
            self.assertTrue(type(cornflakes.eval_datetime(str(x))) in [datetime.datetime, datetime.date, datetime.time])
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
                "20060317",
                "20061703",
                "13:27:54.123",
                "13:27:54",
            ]
        ]
