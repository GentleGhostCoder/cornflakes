from dataclasses import InitVar
import datetime
from decimal import Decimal
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import Optional

from cornflakes.decorator import Index, field
from cornflakes.decorator.dataclasses import AnyUrl, config


class ExampleEnum(Enum):
    sample = "abc"


@config(
    files="tests/configs/default.ini",
    sections="sub_config",
    use_regex=True,
    is_list=True,
    frozen=True,
    eval_env=True,
    validate=True,
    chain_files=True,
)
class SubConfigClass:
    """Test Config Class."""

    url: AnyUrl = field(
        no_default=True,
    )
    init_config: InitVar[Optional[bool]] = field(default=None)
    idx_at5: Index = 5  # type: ignore
    idx_at_first_ini_or_0: Index["SubConfigClass"] = 0  # type: ignore
    test: Optional[str] = None
    section_name: str = ""
    string: str = "bla123"
    empty_string: str = ""
    datetime_datetime: datetime.datetime = datetime.datetime(2006, 3, 17, 13, 27, 54, tzinfo=datetime.timezone.utc)
    datetime_time: datetime.time = datetime.time(13, 27, 54, tzinfo=datetime.timezone.utc)
    int_val: int = 1
    float_val: float = 0.005
    decimal: Decimal = Decimal("0.0000000000000000000000000000000000000001")
    ipv4: IPv4Address = IPv4Address("127.0.0.1")
    ipv6: IPv6Address = IPv6Address("684D:1111:222:3333:4444:5555:6:77")
    bool_val: bool = True
    enum: ExampleEnum = ExampleEnum.sample
    some_env: str = field(default="default_value", aliases=["some_env"], ignore=True)
    lineterminator: str = "\n"
    escapechar: str = "\\"
    quotechar: str = '"'
    sep: str = ","
    euro: str = "€"
