from datetime import datetime, timezone, timedelta
import tzlocal
import zoneinfo
import dateutil
import pandas
import calendar
import pytz

def to_timezone(dt, timezone=None):
    """
    Converts a datetime.datetime to a different time-zone.
    If no timezone is specified, the time is assumed to be local time-zone as retrieved via tzlocal.get_localzone().
    If the timezone is not specified or is None, the local timezone will be used as the resulting timezone.

    As a result, this function can be used to market a naive datetime to the local timezone.
    >>> import datetime
    >>> now = datetime.datetime.now()
    >>> now
    ... datetime.datetime(2016, 5, 10, 12, 0, 0)
    >>> zoned_now = to_timezone(now)
    >>> zoned_now
    ... datetime.datetime(2016, 5, 10, 12, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>)
    which is equal to:
    >>> import pytz
    >>> zoned_now = to_timezone(now, pytz.timezone('Europe/Amsterdam'))
    >>> to_timezone(now, pytz.timezone('Europe/Amsterdam'))
    ... datetime.datetime(2016, 5, 10, 12, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>)

    Naive or not, we can convert any datetime to any timezones defined in pytz.
    >>> to_timezone(now, pytz.timezone('US/Pacific'))
    ... datetime.datetime(2016, 5, 10, 12, 0, 0, tzinfo=<DstTzInfo 'US/Pacific' PDT-1 day, 17:00:00 DST>)

    Note that this result matches exactly the time-zoned datetime.
    >>> to_timezone(zeond_utc, timezone=pytz.UTC)
    ... datetime.datetime(2016, 5, 10, 12, 0, 0, tzinfo=<UTC>)

    Going through UTC is mostly unnecessary.
    >>> to_timezone(now, timezone=pytz.timezone("Europe/London"))
    ... datetime.datetime(2016, 5, 10, 11, 0, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
    >>> to_timezone(now, timezone=pytz.timezone("Asia/Tokyo"))
    ... datetime.datetime(2016, 5, 10, 20, 0, 0, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00>)

    :param dt: datetime.datetime
    :param timezone: Target time-zone. Defaults to the local time-zone as default by the to_timezone method
    :param is_dst: True if the time is in daylight saving time, False if not, None if unknown
    :return: datetime.datetime
    """
    tz = tzlocal.get_localzone()
    if dt.tzinfo is None and timezone is None:
        return dt.astimezone(tz)
    else:
        dt.astimezone(timezone)
    return dt

def from_posix_micros(posix, tz=None):
    """
    Converts a posix micro-seconds to a datetime.datetime.
    If no timezone is specified, the time is assumed to be local time-zone.
    :param posix: posix micro-seconds
    :param timezone: Target time-zone. Defaults to the local time-zone as default by the to_timezone method
    :return: datetime.datetime
    """
    seconds = posix / 1000000
    micros = posix % 1000000
    utc_dt = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=seconds,microseconds=micros)
    return to_timezone(utc_dt, tz)

def to_posix_micros(dt, tz=None):
    """
    Converts a datetime.datetime to a posix micro-seconds.
    If no timezone is specified, the time is assumed to be local time-zone.
    :param dt: datetime.datetime
    :param timezone: Target time-zone. Defaults to the local time-zone as default by the to_timezone method
    :return: posix micro-seconds
    """
    if tz is None:
        utc_dt = to_timezone(dt, timezone=pytz.UTC)
    else:
        utc_dt = to_timezone(dt, timezone=timezone)
    return calendar.timegm(utc_dt.timetuple()) * 1000000 + utc_dt.microsecond

def now(timezone=None):
    """
    Returns the current time in the specified timezone.
    If no timezone is specified, the time is assumed to be local time-zone.
    :param timezone: Target time-zone. Defaults to the local time-zone as default by the to_timezone method
    :return: datetime.datetime
    """
    return to_timezone(datetime.now(), timezone)