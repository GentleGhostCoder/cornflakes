import datetime
from typing import Optional, cast


def _check_milliseconds_field(millisecond) -> None:
    if not 0 <= millisecond <= 999:
        raise ValueError("microsecond must be in 0..999", millisecond)


class DatetimeMS(datetime.datetime):
    """Class for datetime with milliseconds instead of microseconds."""

    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0, millisecond=0, tzinfo=None, *, fold=0):
        """Class for datetime with milliseconds instead of microseconds.

        :param year: int
        :param month: int
        :param day: int
        :param hour: int
        :param minute: int
        :param second: int
        :param millisecond: int
        :param tzinfo: datetime.tzinfo
        :param fold: int

        :return: Datetime instance
        :rtype: DatetimeMS
        """
        _check_milliseconds_field(millisecond)
        self: datetime.datetime = datetime.datetime.__new__(
            cls, year, month, day, hour, minute, second, millisecond * 1000, tzinfo
        )

        return self

    def __repr__(self):
        """Convert to formal string, for repr()."""
        datetime_list = [
            self.year,
            self.month,
            self.day,  # These are never zero
            self.hour,
            self.minute,
            self.second,
            self.millisecond,
        ]
        if datetime_list[-1] == 0:
            del datetime_list[-1]
        if datetime_list[-1] == 0:
            del datetime_list[-1]
        datetime_str = f"datetime_ms({', '.join(map(str, datetime_list))})"
        if self.tzinfo is not None and datetime_str[-1:] == ")":
            datetime_str = datetime_str[:-1] + ", tzinfo=%r" % self.tzinfo + ")"
        if self.fold and datetime_str[-1:] == ")":
            datetime_str = f"{datetime_str[:-1]}, fold=1)"
        return datetime_str

    @property
    def millisecond(self) -> int:
        """Milliseconds of datetime.

        :return: milliseconds
        :rtype: int
        """
        return int(self.microsecond / 1000)

    def __str__(self):
        """Convert to string, for str()."""
        return self.isoformat(sep=" ", timespec="milliseconds")[:-3]


def datetime_ms(
    year,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = 0,
    minute: Optional[int] = 0,
    second: Optional[int] = 0,
    millisecond: Optional[int] = 0,
    tzinfo: Optional[datetime.tzinfo] = None,
) -> DatetimeMS:
    """Create Instance of :meth:`cornflakes.common.DatetimeMS`."""
    return cast(DatetimeMS, DatetimeMS(year, month, day, hour, minute, second, millisecond, tzinfo))  # camelcase
