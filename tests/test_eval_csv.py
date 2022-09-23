import unittest
from datetime import datetime, time

import cornflakes


class TestEvalDatetime(unittest.TestCase):
    """Tests for eval_csv."""

    def test_csv_bytes_types(self):
        self.assertEqual(
            cornflakes.eval_csv(
                "int_col,bool_col,datetime_ms_col,datetime_col,"
                "time_col,text_with_quoted_seperator_col,None\n"
                "1,TRUE,'20060317 13:27:54.123','20060317 13:27:54.123456',"
                "'13:27:54.123','blabla ,blublub',NA\n"
            ),
            {
                "content_length": 185,
                "line_seperator": "\n",
                "line_count": 2,
                "column_seperator": ",",
                "column_count": 7,
                "schema": [
                    {"name": "int_col", "position": 0, "types": [int]},
                    {"name": "bool_col", "position": 1, "types": [bool]},
                    {"name": "datetime_ms_col", "position": 2, "types": [cornflakes.DatetimeMS]},
                    {"name": "datetime_col", "position": 3, "types": [datetime]},
                    {"name": "time_col", "position": 4, "types": [time]},
                    {
                        "name": "text_with_quoted_seperator_col",
                        "position": 5,
                        "types": [str],
                    },
                    {"name": "None", "position": 6, "types": [type(None)]},
                ],
            },
        )

    def test_csv_bytes_col_names(self):
        self.assertEqual(
            cornflakes.eval_csv("invalid_column?\n"),
            {
                "content_length": 16,
                "line_seperator": "\n",
                "line_count": 1,
                "column_seperator": ",",
                "column_count": 1,
                "schema": [{"name": None, "position": 0, "types": [str]}],
            },
        )
