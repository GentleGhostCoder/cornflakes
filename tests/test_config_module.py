import datetime
from decimal import Decimal
from importlib import import_module
from ipaddress import IPv4Address, IPv6Address
from os import environ
import pathlib
import time
import unittest

from cornflakes.builder import generate_config_group_module
from cornflakes.decorator.dataclasses import AnyUrl
from cornflakes.types import Loader
from tests import configs


class TestConfigGeneration(unittest.TestCase):
    """Test-class config module generation"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_auto_config_generation(self):
        """Test-function config module generation."""

        source_config = "tests/configs/default.ini"
        target_module_file = "tests/configs/default.py"
        test_file = "tests/configs/default.py.txt"
        ini_group_args = {"files": "tests/configs/default.ini", "eval_env": True}

        generate_config_group_module(
            class_name="MainConfig",
            source_module=configs.sub_config,
            source_config=source_config,
            target_module_file=target_module_file,
            loader=Loader.INI,
            **ini_group_args
        )

        generated_config_module = pathlib.Path(target_module_file).read_text()
        defined_config_module = pathlib.Path(test_file).read_text()
        self.assertEqual(generated_config_module, defined_config_module)

        MainConfig = import_module("tests.configs.default").MainConfig

        main_config = MainConfig()

        # config_dict = {
        #     'bootstrap_servers': 'localhost',
        #     'client_id': 'kafka-python-' + "1.0.0",
        #     'group_id': None,
        #     'key_deserializer': None,
        #     'value_deserializer': None,
        #     'fetch_max_wait_ms': 500,
        #     'fetch_min_bytes': 1,
        #     'fetch_max_bytes': 52428800,
        #     'max_partition_fetch_bytes': 1 * 1024 * 1024,
        #     'request_timeout_ms': 305000, # chosen to be higher than the default of max_poll_interval_ms
        #     'retry_backoff_ms': 100,
        #     'reconnect_backoff_ms': 50,
        #     'reconnect_backoff_max_ms': 1000,
        #     'max_in_flight_requests_per_connection': 5,
        #     'auto_offset_reset': 'latest',
        #     'enable_auto_commit': True,
        #     'auto_commit_interval_ms': 5000,
        #     'default_offset_commit_callback': lambda offsets, response: True,
        #     'check_crcs': True,
        #     'metadata_max_age_ms': 5 * 60 * 1000,
        #     'max_poll_records': 500,
        #     'max_poll_interval_ms': 300000,
        #     'session_timeout_ms': 10000,
        #     'heartbeat_interval_ms': 3000,
        #     'receive_buffer_bytes': None,
        #     'send_buffer_bytes': None,
        #     'socket_options': [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)],
        #     'sock_chunk_bytes': 4096,  # undocumented experimental option
        #     'sock_chunk_buffer_count': 1000,  # undocumented experimental option
        #     'consumer_timeout_ms': float('inf'),
        #     'security_protocol': 'PLAINTEXT',
        #     'ssl_context': None,
        #     'ssl_check_hostname': True,
        #     'ssl_cafile': None,
        #     'ssl_certfile': None,
        #     'ssl_keyfile': None,
        #     'ssl_crlfile': None,
        #     'ssl_password': None,
        #     'ssl_ciphers': None,
        #     'api_version': None,
        #     'api_version_auto_timeout_ms': 2000,
        #     'connections_max_idle_ms': 9 * 60 * 1000,
        #     'metric_reporters': [],
        #     'metrics_num_samples': 2,
        #     'metrics_sample_window_ms': 30000,
        #     'metric_group_prefix': 'consumer',
        #     'selector': selectors.DefaultSelector,
        #     'exclude_internal_topics': True,
        #     'sasl_mechanism': None,
        #     'sasl_plain_username': None,
        #     'sasl_plain_password': None,
        #     'sasl_kerberos_service_name': 'kafka',
        #     'sasl_kerberos_domain_name': None,
        #     'sasl_oauth_token_provider': None,
        #     'legacy_iterator': False, # enable to revert to < 1.4.7 iterator
        # }
        # generate_config_module(
        #     "KafkaConsumerConfig",
        #     config_dict,
        #     target_module_file="test_config_module.py",
        #     module_description="Auto generated KafkaConsumerConfig Class from kafka module.",
        #     class_description="KafkaConsumerConfig class for kafka module.",
        #     frozen=True,
        # )

        def main_config_passing(config: MainConfig):
            return config

        main_config_passing(main_config)

        def dict_passing(**kwargs):
            return kwargs

        self.assertEqual(MainConfig().to_dict(), dict_passing(**main_config))

        self.assertEqual(
            MainConfig().to_dict(),
            {
                "sub_config_class": [
                    {
                        "url": "https://localhost:8080",
                        "idx_at5": 5,
                        "idx_at_first_ini_or_0": 5,
                        "test": None,
                        "section_name": "sub_config_0",
                        "string": "bla0",
                        "empty_string": "",
                        "datetime_datetime": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        "datetime_time": datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        "int_val": 1,
                        "float_val": 0.005,
                        "decimal": Decimal("1E-40"),
                        "ipv4": IPv4Address("127.0.0.1"),
                        "ipv6": IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        "bool_val": True,
                        "enum": configs.sub_config.ExampleEnum.sample,
                        "some_env": "default_value",
                        "lineterminator": "\n",
                        "escapechar": "\\",
                        "quotechar": '"',
                        "sep": ",",
                        "euro": "€",
                    },
                    {
                        "url": "https://localhost:8080",
                        "idx_at5": 6,
                        "idx_at_first_ini_or_0": 6,
                        "test": None,
                        "section_name": "sub_config_1",
                        "string": "bla1",
                        "empty_string": "",
                        "datetime_datetime": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        "datetime_time": datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        "int_val": 1,
                        "float_val": 0.005,
                        "decimal": Decimal("1E-40"),
                        "ipv4": IPv4Address("127.0.0.1"),
                        "ipv6": IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        "bool_val": False,
                        "enum": configs.sub_config.ExampleEnum.sample,
                        "some_env": "default_value",
                        "lineterminator": "\n",
                        "escapechar": "\\",
                        "quotechar": '"',
                        "sep": ",",
                        "euro": "€",
                    },
                    {
                        "url": "https://localhost:8080",
                        "idx_at5": 7,
                        "idx_at_first_ini_or_0": 7,
                        "test": None,
                        "section_name": "sub_config_2",
                        "string": "bla2",
                        "empty_string": "",
                        "datetime_datetime": datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        "datetime_time": datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        "int_val": 1,
                        "float_val": 0.005,
                        "decimal": Decimal("1E-40"),
                        "ipv4": IPv4Address("127.0.0.1"),
                        "ipv6": IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        "bool_val": False,
                        "enum": configs.sub_config.ExampleEnum.sample,
                        "some_env": "default_value",
                        "lineterminator": "\n",
                        "escapechar": "\\",
                        "quotechar": '"',
                        "sep": ",",
                        "euro": "€",
                    },
                ]
            },
        )

        self.assertEqual(MainConfig().to_tuple(), (*MainConfig(),))

        self.assertEqual(
            MainConfig().to_tuple(),
            (
                [
                    (
                        "https://localhost:8080",
                        5,
                        5,
                        None,
                        "sub_config_0",
                        "bla0",
                        "",
                        datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        1,
                        0.005,
                        Decimal("1E-40"),
                        IPv4Address("127.0.0.1"),
                        IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        True,
                        configs.sub_config.ExampleEnum.sample,
                        "default_value",
                        "\n",
                        "\\",
                        '"',
                        ",",
                        "€",
                    ),
                    (
                        "https://localhost:8080",
                        6,
                        6,
                        None,
                        "sub_config_1",
                        "bla1",
                        "",
                        datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        1,
                        0.005,
                        Decimal("1E-40"),
                        IPv4Address("127.0.0.1"),
                        IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        False,
                        configs.sub_config.ExampleEnum.sample,
                        "default_value",
                        "\n",
                        "\\",
                        '"',
                        ",",
                        "€",
                    ),
                    (
                        "https://localhost:8080",
                        7,
                        7,
                        None,
                        "sub_config_2",
                        "bla2",
                        "",
                        datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                        datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                        1,
                        0.005,
                        Decimal("1E-40"),
                        IPv4Address("127.0.0.1"),
                        IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                        False,
                        configs.sub_config.ExampleEnum.sample,
                        "default_value",
                        "\n",
                        "\\",
                        '"',
                        ",",
                        "€",
                    ),
                ],
            ),
        )

        # list(MainConfig.from_ini(filter_function=lambda x: x.string == "bla0").sub_config)
        MainConfig().to_ini("tests/configs/default_auto_created.ini")

        time.sleep(1)

        self.assertEqual(
            repr(MainConfig(files="tests/configs/default_auto_created.ini")),
            repr(MainConfig(files="tests/configs/default.ini")),
        )

        environ["some_env"] = "test123"

        self.assertEqual(
            repr(configs.sub_config.SubConfigClass.from_ini("tests/configs/default.ini")),
            repr(
                {
                    "sub_config_class": [
                        configs.sub_config.SubConfigClass(
                            url=AnyUrl(
                                scheme="https",
                                netloc="localhost:8080",
                                path="",
                                query="",
                                params="",
                                query_args={},
                                fragment="",
                                token=None,
                            ),
                            idx_at_first_ini_or_0=5,
                            test=None,
                            section_name="sub_config_0",
                            string="bla0",
                            empty_string="",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=True,
                            enum=configs.sub_config.ExampleEnum.sample,
                            some_env="test123",
                            lineterminator="\n",
                            escapechar="\\",
                            quotechar='"',
                            sep=",",
                            euro="€",
                        ),
                        configs.sub_config.SubConfigClass(
                            test=None,
                            section_name="sub_config_1",
                            string="bla1",
                            empty_string="",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=False,
                            url=AnyUrl(
                                scheme="https",
                                netloc="localhost:8080",
                                path="",
                                query="",
                                params="",
                                query_args={},
                                fragment="",
                                token=None,
                            ),
                            enum=configs.sub_config.ExampleEnum.sample,
                            some_env="test123",
                            lineterminator="\n",
                            escapechar="\\",
                            quotechar='"',
                            sep=",",
                            euro="€",
                        ),
                        configs.sub_config.SubConfigClass(
                            test=None,
                            section_name="sub_config_2",
                            string="bla2",
                            empty_string="",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=False,
                            url=AnyUrl(
                                scheme="https",
                                netloc="localhost:8080",
                                path="",
                                query="",
                                params="",
                                query_args={},
                                fragment="",
                                token=None,
                            ),
                            enum=configs.sub_config.ExampleEnum.sample,
                            some_env="test123",
                            lineterminator="\n",
                            escapechar="\\",
                            quotechar='"',
                            sep=",",
                            euro="€",
                        ),
                    ]
                }
            ),
        )

        self.assertEqual(
            repr(MainConfig()),
            repr(
                MainConfig(
                    sub_config_class=[
                        configs.sub_config.SubConfigClass(
                            idx_at_first_ini_or_0=5,
                            test=None,
                            section_name="sub_config_0",
                            string="bla0",
                            empty_string="",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=True,
                            url=AnyUrl(
                                scheme="https",
                                netloc="localhost:8080",
                                path="",
                                query="",
                                params="",
                                query_args={},
                                fragment="",
                                token=None,
                            ),
                            enum=configs.sub_config.ExampleEnum.sample,
                            some_env="test123",
                            lineterminator="\n",
                            escapechar="\\",
                            quotechar='"',
                            sep=",",
                            euro="€",
                        ),
                        configs.sub_config.SubConfigClass(
                            test=None,
                            section_name="sub_config_1",
                            string="bla1",
                            empty_string="",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=False,
                            url=AnyUrl(
                                scheme="https",
                                netloc="localhost:8080",
                                path="",
                                query="",
                                params="",
                                query_args={},
                                fragment="",
                                token=None,
                            ),
                            enum=configs.sub_config.ExampleEnum.sample,
                            some_env="test123",
                            lineterminator="\n",
                            escapechar="\\",
                            quotechar='"',
                            sep=",",
                            euro="€",
                        ),
                        configs.sub_config.SubConfigClass(
                            test=None,
                            section_name="sub_config_2",
                            string="bla2",
                            empty_string="",
                            datetime_datetime=datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc),
                            datetime_time=datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc),
                            int_val=1,
                            float_val=0.005,
                            decimal=Decimal("1E-40"),
                            ipv4=IPv4Address("127.0.0.1"),
                            ipv6=IPv6Address("684d:1111:222:3333:4444:5555:6:77"),
                            bool_val=False,
                            url=AnyUrl(
                                scheme="https",
                                netloc="localhost:8080",
                                path="",
                                query="",
                                params="",
                                query_args={},
                                fragment="",
                                token=None,
                            ),
                            enum=configs.sub_config.ExampleEnum.sample,
                            some_env="test123",
                            lineterminator="\n",
                            escapechar="\\",
                            quotechar='"',
                            sep=",",
                            euro="€",
                        ),
                    ]
                )
            ),
        )
