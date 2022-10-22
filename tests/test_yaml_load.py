import datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
import os
import unittest

import cornflakes


class TestIniLoad(unittest.TestCase):
    """Tests for ini_load."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None
        os.environ["ENV_VAR1"] = "blabla"

    def test_ini_load_examples1(self):
        self.assertEqual(
            cornflakes.yaml_load(files=["tests/configs/default.yaml", "tests/configs/logging.yaml"]),
            {
                "tests/configs/default.yaml": {
                    "test": {
                        "bool": True,
                        "datetime_datetime": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        "datetime_time": datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        "decimal": Decimal("1E-40"),
                        "float": 0.005,
                        "int": 1,
                        "ipv4": IPv4Address("127.0.0.1"),
                        "ipv6": IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        "string": "bla0",
                    },
                    "test1": {
                        "bool": True,
                        "datetime_datetime": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        "datetime_time": datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        "decimal": Decimal("1E-40"),
                        "float": 0.005,
                        "int": 1,
                        "ipv4": IPv4Address("127.0.0.1"),
                        "ipv6": IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        "string": "bla1",
                    },
                    "test2": {
                        "bool": True,
                        "datetime_datetime": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        "datetime_time": datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        "decimal": Decimal("1E-40"),
                        "float": 0.005,
                        "int": 1,
                        "ipv4": IPv4Address("127.0.0.1"),
                        "ipv6": IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        "string": "bla2",
                    },
                }
            },
        )

    def test_ini_load_examples2(self):
        self.assertEqual(
            cornflakes.yaml_load(
                files={"default": ["tests/configs/default.yaml", "tests/configs/logging.yaml"]},
                sections=["test", "test3", "handlers"],
                keys={"ip4v": ["ip4v"], "handlers": ["handlers", "formatters"], "not_existing": "not_existing"},
                defaults={
                    "not_existing": True,
                },
            ),
            {
                "default": {
                    "test": {"ip4v": None, "handlers": None, "not_existing": True},
                    "test3": {"ip4v": None, "handlers": None, "not_existing": True},
                    "handlers": {"ip4v": None, "handlers": None, "not_existing": True},
                }
            },
        )
