import unittest

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
                "column_count": 7,
                "column_separator": ",",
                "column_types": ["int", "bool", "datetime", "datetime", "time", "str", "NoneType"],
                "has_header": "True",
                "header": [
                    "int_col",
                    "bool_col",
                    "datetime_ms_col",
                    "datetime_col",
                    "time_col",
                    "text_with_quoted_seperator_col",
                    "None",
                ],
                "line_separator": "\n",
                "parsed_line_count": 2,
                "quoting_character": "'",
            },
        )

    def test_csv_bytes_col_names(self):
        self.assertEqual(
            cornflakes.eval_csv("invalid_column,,123,'bla,blub'\n", ".!@#$%^&*()+?=<>/\\ "),
            {
                "column_count": 4,
                "column_separator": ",",
                "column_types": ["str", "NoneType", "int", "str"],
                "has_header": "False",
                "line_separator": "\n",
                "parsed_line_count": 1,
                "quoting_character": "'",
            },
        )
