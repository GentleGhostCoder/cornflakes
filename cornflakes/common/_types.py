import datetime


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
        self = datetime.datetime.__new__(cls, year, month, day, hour, minute, second, millisecond * 1000, tzinfo)
        return self

    @property
    def millisecond(self) -> int:
        """Milliseconds of datetime.

        :return: milliseconds
        :rtype: int
        """
        return int(self.microsecond / 1000)

    def __str__(self):
        """Convert to string, for str()."""
        return self.isoformat(sep=" ")[:-3]


def datetime_ms(
    year,
    month: int = None,
    day: int = None,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    millisecond: int = 0,
    tzinfo: datetime.tzinfo = None,
) -> DatetimeMS:
    """Create Instance of :meth:`cornflakes._types.DatetimeMS`."""
    return DatetimeMS(year, month, day, hour, minute, second, millisecond, tzinfo)  # camelcase
