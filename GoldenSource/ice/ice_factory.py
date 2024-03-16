from datetime import datetime, date
from GoldenSource.time import from_posix_micros, to_posix_micros, to_timezone
from GS.dataobjects import IDate, IDateTime
from GoldenSource.utils.patterns import cache_result
import pandas

DATE_FMT = "%Y-%m-%d"
TIME_FMT = "%H:%M:%S.%f"
RUNID_FMT = "%H%M"


@cache_result
def make_idate(idate=None):
    if idate is None:
        return IDate()
    if type(idate) is IDate:
        return idate
    
    if type(idate) is not date:
        if type(idate) is datetime:
            idate = date2idate(idate.date())
        elif type(idate) is pandas.Timestamp:
            idate = date2idate(idate.to_pydatetime().date())
        elif type(idate) is IDateTime:
            idate = date2idate(idatetime_to_datetime(idate).date())
        else:
            idate = date2idate(datetime.strptime(str(idate)[:10], DATE_FMT).date())
    else:
        idate = date2idate(idate)
    return idate

def date2idate(date):
    if date is None:
        return None
    
    return IDate(int(date.strftime("%Y%m%d")))

def idate2date(idate):
    if idate is None:
        return None
    return datetime.strptime(str(idate.yyyyMMdd), "%Y%m%d").date()

def idatetime_to_datetime(idt, timezone=None):
    """
    Converts a IDateTime to a datetime.
    The target time-zone can be specified as a parameter. If None is psecified, 
    see time.from_posix_micro for information on the default behavior.
    :param idt: IDateTime to convert
    :param timezone: Target time-zone
    :return: datetime
    """
    if idt is None:
        return None
    
    return from_posix_micros(idt.val, timezone)

def datetime_to_idatetime(dt):
    """
    Converts a datetime to a IDateTime.
    :param dt: datetime to convert
    :return: IDateTime
    """
    if dt is None:
        return None
    
    return IDateTime(to_posix_micros(dt))