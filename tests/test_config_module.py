import datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
from os import environ
import time
import unittest

from cornflakes.builder import generate_group_module
from tests import configs


class TestConfigGeneration(unittest.TestCase):
    """Test-class config module generation"""

    def test_auto_config_generation(self):
        """Test-function config module generation."""

        source_config = "tests/configs/default.ini"
        target_module_file = "tests/configs/default.py"
        test_file = "tests/configs/default.py.txt"
        ini_group_args = {"files": "tests/configs/default.ini", "eval_env": True}

        generate_group_module(
            class_name="MainConfig",
            source_module=configs.sub_config,
            source_config=source_config,
            target_module_file=target_module_file,
            **ini_group_args
        )

        with open(target_module_file) as file:
            generated_config_module = file.read()
        with open(test_file) as file:
            defined_config_module = file.read()

        self.assertEqual(generated_config_module, defined_config_module)

        from tests.configs.default import MainConfig

        MainConfig.from_ini()

        # list(MainConfig.from_ini(filter_function=lambda x: x.string == "bla0").sub_config)
        MainConfig.from_ini().to_ini("tests/configs/default_auto_created.ini")

        time.sleep(1)

        self.assertEqual(
            repr(MainConfig.from_ini("tests/configs/default_auto_created.ini")),
            repr(MainConfig.from_ini("tests/configs/default.ini")),
        )

        environ["some_env"] = "test123"

        self.assertEqual(
            repr(configs.sub_config.SubConfig.from_ini("tests/configs/default.ini")),
            repr(
                {
                    "sub_config": [
                        configs.sub_config.SubConfig(
                            section_name="sub_config_0",
                            string="bla0",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=True,
                            some_env="test123",
                        ),
                        configs.sub_config.SubConfig(
                            section_name="sub_config_1",
                            string="bla1",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=True,
                            some_env="test123",
                        ),
                        configs.sub_config.SubConfig(
                            section_name="sub_config_2",
                            string="bla2",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=True,
                            some_env="test123",
                        ),
                    ]
                }
            ),
        )

        self.assertEqual(
            repr(MainConfig.from_ini()),
            repr(
                MainConfig(
                    sub_config=[
                        configs.sub_config.SubConfig(
                            section_name="sub_config_0",
                            string="bla0",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=True,
                            some_env="default_value",
                        ),
                        configs.sub_config.SubConfig(
                            section_name="sub_config_1",
                            string="bla1",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=True,
                            some_env="default_value",
                        ),
                        configs.sub_config.SubConfig(
                            section_name="sub_config_2",
                            string="bla2",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=True,
                            some_env="default_value",
                        ),
                    ]
                )
            ),
        )
