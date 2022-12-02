from dataclasses import InitVar
import datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address

from cornflakes import AnyUrl, config, config_field
from cornflakes.decorator import field


@config(sections=None, use_regex=True, is_list=True, frozen=True, eval_env=True, validate=True)
class SubConfig:
    """Test Config Class."""

    init_config: InitVar[bool] = True
    section_name: str = ""
    string: str = "bla123"
    datetime_datetime: datetime.datetime = datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc)
    datetime_time: datetime.time = datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc)
    int_val: int = 1
    float_val: float = 0.005
    decimal: Decimal = Decimal("0.0000000000000000000000000000000000000001")
    ipv4: IPv4Address = IPv4Address("127.0.0.1")
    ipv6: IPv6Address = IPv6Address("684D:1111:222:3333:4444:5555:6:77")
    bool_val: bool = True
    url: AnyUrl = field(
        no_default=True,
    )
    some_env: str = field(default="default_value", alias=["some_env"], ignore=True)
