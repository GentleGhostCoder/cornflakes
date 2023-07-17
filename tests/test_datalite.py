from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Dict, Generator, List, Tuple
from uuid import UUID

from cornflakes.decorator import field
from cornflakes.decorator.dataclasses import dataclass as data
from cornflakes.decorator.datalite.datalite_decorator import datalite


class StatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


def test_datalite():
    """Test datalite decorator."""

    def generator_function() -> Generator[int, None, None]:
        yield from range(10)

    @datalite(db_path="test_datalite.db")
    @data(
        dict_factory=None,
        tuple_factory=None,
        slots=False,  # TODO: add obj_id to slots if using db_path
        eval_env=True,
        validate=True,
        updatable=True,
    )
    class TestDataLite:
        string_value: str = "blub"
        integer_value: int = 0
        float_value: float = float(0.0)
        bytes_value: bytes = b"blub"
        bool_value: bool = False
        uuid_value: UUID = UUID("00000000-0000-0000-0000-000000000000")
        datetime_value: datetime = datetime.now()
        date_value: date = datetime.now().date()
        time_value: time = datetime.now().time()
        decimal_value: Decimal = Decimal("0.00")
        list_value: List[str] = field(default_factory=list)
        dict_value: Dict[str, Any] = field(default_factory=dict)
        tuple_value: Tuple[int, str] = field(default_factory=lambda: (1, "blub"))
        ipv4_value: IPv4Address = IPv4Address("192.0.2.0")
        ipv6_value: IPv6Address = IPv6Address("2001:db8::1")
        enum_value: StatusEnum = StatusEnum.ACTIVE
        complex_value: complex = 1 + 2j
        # set_value: set = field(default_factory=lambda: {1, 2, 3})
        # frozenset_value: frozenset = field(default_factory=lambda: frozenset({1, 2, 3}))
        # bytearray_value: bytearray = bytearray(b"hello")
        # memoryview_value: memoryview = memoryview(b"world")
        # slice_value: slice = slice(1, 5, 2)
        # range_value: range = range(0, 10, 2)
        # classmethod_value: classmethod = classmethod(lambda cls: print("classmethod called"))
        # any_value: Any = "anything"
        # type_value: Type[int] = int
        # callable_value: Callable[[int, int], int] = lambda x, y: x + y
        # generator_value: Generator[int, None, None] = generator_function()
        # optional_value: Optional[int] = None
        # union_value: Union[int, str] = "blub"

    test = TestDataLite()
    test.create_entry()


# TODO:
# - add obj_id to slots
# - check that no field of __dataclass_fields__ overrides the annotation type or dataclass type
