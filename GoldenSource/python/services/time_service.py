import datetime

import GS.dataobjects as do
from GoldenSource.python.ice.ice_factory import make_idate, make_idatetime, idate2date, idatetime_to_datetime
from GoldenSource.python.utils.patterns import cache_result
from GoldenSource.python.common.services import Service
import dateutil.parser


@cache_result
def convert_date(dt, as_type=None):
    """
    Converts a date to the type specified by as_type. If as_type is None, it will return the date as a datetime.date object.
    Supported types:
        - datetime.date
        - datetime.datetime
        - str
        - IDate
        - IDateTime
        - int
    """

    assert isinstance(dt, datetime.date), "Expected date of type [datetime.date], got [{0}]".format(type(dt).__name__)

    if as_type is None:
        return dt
    elif issubclass(as_type, datetime.datetime):
        return datetime.datetime.combine(dt, datetime.time())
    elif issubclass(as_type, datetime.date):
        return dt
    elif issubclass(as_type, do.IDate):
        return make_idate(dt)
    elif issubclass(as_type, do.IDateTime):
        return make_idatetime(dt)
    elif issubclass(as_type, str):
        return dt.isoformat()
    elif issubclass(as_type, int):
        return as_type(dt.strftime('%Y%m%d'))
    return None

@cache_result
def read_date(dt=None):
    """
    Reads the date from a number of various formats.
    Returns a datetime.date
    """
    if dt is None:
        return datetime.date.today()
    elif isinstance(dt, datetime.datetime):
        return dt.date()
    elif isinstance(dt, datetime.date):
        return dt    
    elif isinstance(dt, do.IDate):
        return idate2date(dt)
    elif isinstance(dt, do.IDateTime):
        return idatetime_to_datetime(dt)
    elif isinstance(dt, int):
        return datetime.datetime.strptime(str(dt), '%Y%m%d').date()
    elif isinstance(dt, str):
        return dateutil.parser.parse(dt).date()
    return None

@cache_result # Due to no hash issue for calendar
def nearest_business_day(offset=0, refdate=datetime.date.today(), calendar=None):
    """
    Returns the nearest business day to the date specified.
    """
    day = refdate + datetime.timedelta(offset)
    return next_business_day(0, day, calendar)

@cache_result # Due to no hash issue for calendar
def next_business_day(offset=0, refdate=datetime.date.today(), calendar=None):
    """
    Returns the nth business day from refdate taking the calendar into account.
    if offset is 0, returns the refdate if it is a business day or the *previous* business day.
    """
    if offset > 0:
        step = 1
    else:
        step = -1
    
    is_cal_legit = calendar and calendar.holidays
    if offset != 0:
        day = next_business_day(offset=0, refdate=refdate, calendar=calendar)
    else:
        day = refdate

    day_off = datetime.timedelta(step)
    bus_counter = 0
    go_on = True
    while go_on:
        if day.weekday() in (5, 6):
            day += datetime.timedelta(step * 1.5 + 0.5 - (day.weekday() - 5))
        elif is_cal_legit and make_idate(day) in calendar.holidays:
            day += day_off
        else:
            bus_counter += 1
            if bus_counter <= abs(offset):
                day += day_off
            else:
                go_on = False
    return day

###################
### TIME SERVICE ##
###################

class TimeService(Service):
    """
    Convenient centralized service to do all the date/business day computations.
    """
    day_delta = datetime.timedelta(1)
    weekdays = (1, 2, 3, 4, 5)
    weekends = (6, 7)

    def __init__(self, domain) -> None:
        super(TimeService, self).__init__(domain)
        self._refdate = domain.get_param("time_service", 'refdate', default=datetime.date.today())
        self._calendar = domain.get_param("time_service", "calendar", default=None)

        self._today = {True: None, False: None}
        self._yesterday = {True: None, False: None}
        self._day_fct = {True: self.nearest_business_day, False: self.next_calendar_day}
        self._reverse = {True: -1, False: 1}
        self._recompute_dates()
    
    def reference_date(self, as_type=None):
        """
        Returns the reference date as the type specified by as_type. If as_type is None, it will return the date as a datetime.date object.
        Supported types:
            - datetime.datetime
            - str
            - IDate
            - IDateTime
            - int
        """
        return convert_date(self._refdate, as_type)

    def today(self, as_business_day=False, as_type=None):
        """
        Returns the current date as a calendar day or as a business day as the type specified by as_type. 
        If as_type is None, it will return the date as a datetime.date object.
        Supported types:
            - datetime.datetime
            - str
            - IDate
            - IDateTime
            - int
        """
        return convert_date(self._today[as_business_day], as_type)
    
    def now(self, as_business_day=False, as_type=None):
        """
        Returns now as the type specified by as_type. 
        If as_type is None, it will return the date as a datetime.datetime object.
        The major difference with the today() method is that the current time will be set in the value returned.
        Supported types:
            - datetime.datetime
            - str (format "YYYY-MM-DDTHH:MM:SS")
            - IDate
            - IDateTime
            - int
        """
        dt = self._today[as_business_day]
        if as_type is None or issubclass(as_type, datetime.datetime):
            return datetime.datetime.combine(dt, datetime.datetime.now().time())
        elif issubclass(as_type, do.IDateTime):
            return make_idatetime(dt, datetime.datetime.now().time())
        elif issubclass(as_type, str):
            return self.now(as_business_day, datetime.datetime).isoformat()
        elif issubclass(as_type, int):
            now = self.now(as_business_day, datetime.datetime)
            epoch = datetime.datetime(1970, 1, 1)
            secs = int((now - epoch).total_seconds())
            return as_type(secs) * 1000000 + as_type(now.microsecond)
        else:
            return convert_date(dt, as_type)
        
    def yesterday(self, as_business_day=False, as_type=None):
        """
        Returns the previous day as a calendar day or as a business day as the type specified by as_type.
        If as_type is None, it will return the date as a datetime.date object.
        Supported types:
            - datetime.datetime
            - str
            - IDate
            - IDateTime
            - int
        """
        return convert_date(self._yesterday[as_business_day], as_type)
    
    @property
    def calendar(self):
        return self._calendar
    
    def next_day(self, offset=0, as_business_day=False, reverse=False, as_type=None):
        """
        Returns the nth day from today taking the calendar into account.
        if offset is 0, returns the today if it is a business day or the *next* business day.
        Supported types:
            - datetime.datetime
            - str
            - IDate
            - IDateTime
            - int
        """
        return self._day_fct[as_business_day](offset, reverse, as_type)
    
    def next_calendar_day(self, offset=0, reverse=False, as_type=None):
        """
        Returns the nth calendar day from today.
        if offset is 0, returns the today if it is a business day or the *next* business day.
        Supported types:
            - datetime.datetime
            - str
            - IDate
            - IDateTime
            - int
        """
        return convert_date(self._refdate + self.day_delta * offset * self._reverse[reverse], as_type)
    
    def next_weekday(self, offset=0, reverse=False, as_type=None):
        """
        Returns the nth weekday from today.
        if offset is 0, returns the today if it is a business day or the *next* business day.
        Supported types:
            - datetime.datetime
            - str
            - IDate
            - IDateTime
            - int
        """
        return convert_date(nearest_business_day(offset * self._reverse[reverse], self._refdate), as_type)
    
    def nearest_business_day(self, offset=0, reverse=False, as_type=None):
        """
        Returns the nearest business day to the date specified.
        Supported types:
            - datetime.datetime
            - str
            - IDate
            - IDateTime
            - int
        """
        return convert_date(nearest_business_day(offset * self._reverse[reverse], self._refdate, self._calendar), as_type)
    
    def next_business_day(self, offset=0, reverse=False, as_type=None):
        return convert_date(next_business_day(offset * self._reverse[reverse], self._refdate, self._calendar), as_type)

    def offsets2dates(self, offsets, as_business_day=False, reverse=False, as_type=None):
        if offsets is None:
            return None
        elif isinstance(offsets, tuple):
            return tuple(self.next_day(off, as_business_day, reverse, as_type) for off in offsets)
        elif isinstance(offsets, list):
            return list(self.next_day(off, as_business_day, reverse, as_type) for off in offsets)
        elif isinstance(offsets, int):
            return self.next_day(offsets, as_business_day, reverse, as_type)
        return None
    
    def offsets2datelist(self, offsets, as_business_day=False, reverse=False, as_type=None):
        if offsets is None:
            return None
        elif isinstance(offsets, tuple):
            return [set(self.next_day(off, as_business_day, reverse, as_type) for off in range(min(offsets), max(offsets)+1))]
        elif isinstance(offsets, list):
            return [self.next_day(off, as_business_day, reverse, as_type) for off in offsets]
        elif isinstance(offsets, int):
            return [self.next_day(offsets, as_business_day, reverse, as_type)]
        return None
    
    @staticmethod
    def read_date(date, as_type=None):
        """
        Reads the date from a number of various formats.
        Returns a datetime.date
        """
        return convert_date(read_date(date), as_type)
    
    def read_dates(self, dates, as_type=None):
        if dates is None:
            return None
        elif isinstance(dates, tuple):
            return tuple(self.read_date(date, as_type) for date in dates)
        elif isinstance(dates, list):
            return list(self.read_date(date, as_type) for date in dates)
        return self.read_date(dates, as_type)
    
    def set_reference_date(self, refdate):
        self._refdate = refdate
        self._recompute_dates()
    
    def set_calendar(self, calendar):
        """
        Sets the calendar for the TimeService.
        @type calendar: Calendar
        @param calendar: The calendar object to set.
        """
        self._calendar = calendar
        self._recompute_dates()
    
    def _recompute_dates(self):
        self._today[False] = self._refdate
        self._yesterday[False] = self._refdate - self.day_delta
        self._today[True] = self.nearest_business_day(0)
        self._yesterday[True] = self.nearest_business_day(-1)

    def __str__(self) -> str:
        return "ref:{!s}} today:{!s} yesterday:{!s} calendar:{!s}".format(self._refdate, self._today, self._yesterday, self._calendar)
    
    def __repr__(self) -> str:
        return "TimeService({!r}, {!r})".format(self._refdate, self._calendar)
   