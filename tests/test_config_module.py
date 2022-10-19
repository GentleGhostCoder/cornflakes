import datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
from types import ModuleType
import unittest

from cornflakes import ini_config
from cornflakes.config import generate_config_group


@ini_config(sections="test", use_regex=True, frozen=True)
class SubConfig:
    """Test Config Class."""

    string: str = "bla123"
    datetime_datetime: datetime = datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc)
    datetime_time: datetime.time = datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc)
    int: int = 1
    float: float = 0.005
    decimal: Decimal = Decimal("0.0000000000000000000000000000000000000001")
    ip4v: IPv4Address = IPv4Address("127.0.0.1")
    ip6v: IPv6Address = IPv6Address("684D:1111:222:3333:4444:5555:6:77")
    bool: bool = True


class TestEvalDatetime(unittest.TestCase):
    def test_auto_config(self):
        tests = ModuleType("tests")
        tests.test_config_module = ModuleType("tests.test_config_module")
        tests.test_config_module.__dict__.update({"SubConfig": SubConfig})

        template_cfg_file = "tests/configs/default.ini"
        default_cfg_file = "tests/configs/default.ini"
        target_file = "tests/configs/default.py"
        test_file = "tests/configs/default.py.txt"
        generate_config_group(
            name="MainConfig",
            cfg_module=tests.test_config_module,
            template_cfg=template_cfg_file,
            target=target_file,
            cfg_files=default_cfg_file,
        )

        with open(target_file) as file:
            generated_config_module = file.read()
        with open(test_file) as file:
            defined_config_module = file.read()

        self.assertEqual(generated_config_module, defined_config_module)

        main_config = __import__("tests.configs.default").MainConfig

        self.assertEqual(
            repr(main_config.from_ini("tests/configs/default_auto_created.ini")),
            repr(main_config.from_ini("tests/configs/default.ini")),
        )

        self.assertEqual(
            repr(main_config.from_ini()),
            repr(
                main_config(
                    test=SubConfig(
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
                    test1=SubConfig(
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
                    test2=SubConfig(
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
                )
            ),
        )
