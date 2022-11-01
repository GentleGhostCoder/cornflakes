import datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
import logging
import time
import unittest

from cornflakes.builder import generate_group_module
from cornflakes.logging import setup_logging
import tests
from tests.configs import SubConfig


class TestConfigGeneration(unittest.TestCase):
    """Test-class config module generation"""

    def test_auto_config_generation(self):
        """Test-function config module generation."""

        source_config = "tests/configs/default.ini"
        target_module_file = "tests/configs/default.py"
        test_file = "tests/configs/default.py.txt"
        ini_group_args = {"files": "tests/configs/default.ini"}

        generate_group_module(
            class_name="MainConfig",
            source_module=tests.configs.sub_config,
            source_config=source_config,
            target_module_file=target_module_file,
            **ini_group_args
        )

        with open(target_module_file) as file:
            generated_config_module = file.read()
        with open(test_file) as file:
            defined_config_module = file.read()

        self.assertEqual(generated_config_module, defined_config_module)

        MainConfig = __import__("tests.configs.default").configs.default.MainConfig
        list(MainConfig.from_ini(filter_function=lambda x: x.string == "bla0").sub_config)
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
                    sub_config=[
                        SubConfig(
                            section_name="sub_config_0",
                            string="bla0",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int=1,
                            float=0.005,
                            decimal=Decimal("1E-40"),
                            ip4v=IPv4Address("127.0.0.1"),
                            ip6v=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool=True,
                        ),
                        SubConfig(
                            section_name="sub_config_1",
                            string="bla1",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int=1,
                            float=0.005,
                            decimal=Decimal("1E-40"),
                            ip4v=IPv4Address("127.0.0.1"),
                            ip6v=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool=True,
                        ),
                        SubConfig(
                            section_name="sub_config_2",
                            string="bla2",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int=1,
                            float=0.005,
                            decimal=Decimal("1E-40"),
                            ip4v=IPv4Address("127.0.0.1"),
                            ip6v=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool=True,
                        ),
                    ]
                )
            ),
        )
