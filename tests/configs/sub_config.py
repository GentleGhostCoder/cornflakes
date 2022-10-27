import datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address

from cornflakes.decorator.config import config


@config(sections="sub_config", use_regex=True, is_list=True, frozen=True)
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
