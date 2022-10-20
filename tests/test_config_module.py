import datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
import time
import unittest

from cornflakes.config import generate_ini_group_module
import tests
from tests.configs import MainConfig, SubConfig


class TestConfigGeneration(unittest.TestCase):
    """Test-class config module generation"""

    def test_auto_config_generation(self):
        """Test-function config module generation."""
        source_files = "tests/configs/default.ini"
        target_module_file = "tests/configs/default.py"
        test_file = "tests/configs/default.py.txt"
        ini_group_args = {"files": "tests/configs/default.ini"}

        generate_ini_group_module(
            class_name="MainConfig",
            source_module=tests.configs.sub_config,
            source_files=source_files,
            target_module_file=target_module_file,
            **ini_group_args
        )

        with open(target_module_file) as file:
            generated_config_module = file.read()
        with open(test_file) as file:
            defined_config_module = file.read()

        self.assertEqual(generated_config_module, defined_config_module)

        MainConfig.from_ini().to_ini("tests/configs/default_auto_created.ini")

        time.sleep(1)

        self.assertEqual(
            repr(MainConfig.from_ini("tests/configs/default_auto_created.ini")),
            repr(MainConfig.from_ini("tests/configs/default.ini")),
        )

        self.assertEqual(
            repr(MainConfig.from_ini()),
            repr(
                MainConfig(
                    test=SubConfig(
                        string="bla123",
                        datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        int=1,
                        float=0.005,
                        decimal=Decimal("1E-40"),
                        ip4v=IPv4Address("127.0.0.1"),
                        ip6v=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        bool=True,
                    ),
                    test1=SubConfig(
                        string="bla123",
                        datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        int=1,
                        float=0.005,
                        decimal=Decimal("1E-40"),
                        ip4v=IPv4Address("127.0.0.1"),
                        ip6v=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        bool=True,
                    ),
                    test2=SubConfig(
                        string="bla123",
                        datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        int=1,
                        float=0.005,
                        decimal=Decimal("1E-40"),
                        ip4v=IPv4Address("127.0.0.1"),
                        ip6v=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        bool=True,
                    ),
                )
            ),
        )
