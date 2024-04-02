import datetime
import logging
import sys
import os
import traceback

import GS.dataobjects as do
import GS.dataobjects.event as do_evt
import GS.enums.event as en_evt
import dateutil.parser

from GoldenSource.python.ice.ice_factory import make_idate, make_idatetime, idate2date, idatetime_to_datetime

from logging.handlers import RotatingFileHandler
from GoldenSource.python.utils import patterns
from GoldenSource.python.utils.patterns import cache_result
from GoldenSource.python.utils import camelcase_to_underscore

class Service(object):
    """
    Generic service interface. Services are not required to implement this, but it makes things easier.
    """

    def __init__(self, domain) -> None:
        """
        Invoked upon initialization of the service. This will be called once and once only.
        @type domain: Domain
        @param domain: The active domain
        """
        super(Service, self).__init__()
        pass

    def shutdown(self):
        """
        Invoked when the service is being shut down. This will be called once and once only.
        """
        pass

class CacheService(Service):
    """
    Generic cache service
    """
    GETITEM_DEFAULT = object()

    def __init__(self, domain) -> None:
        super(CacheService, self).__init__(domain)
        self._cache = {}

    def _retrieve(self, item):
        raise NotImplementedError('{0.__class__.__name__} does not implement _retrieve'.format(self))
    
    def __getitem__(self, item):
        value = self._cache.get(item)
        if value is None:
            value = self._retrieve(item)
            if value is None:
                raise KeyError(item)
            self._cache[item] = value
        return value
    
    def get(self, item, default=None):
        value = self._cache.get(item)
        if value is None:
            value = self._retrieve(item)
            if value is None:
                value = default
            self._cache[item] = value
        return value

class AggregatorService(Service):
    """
    Service that aggregates multiple subservices into one.
    The DEFAULT_ROUTING class memeber describe the routing that happens. It should be a dictionary 
    mapping a method_name to its service class.
    The constructor that takes over and adequately creates:
        - methods in the Aggregator that match the child service and simply routes to its corresponding method
        - properties to directly access the inner child services directly
    """
    DEFAULT_ROUTING = {}

    def __init__(self, domain) -> None:
        super(AggregatorService, self).__init__(domain)
        self._routing = domain.get_param(self.__class__.__name__, 'routing', default=self.DEFAULT_ROUTING)

        for service_class in set(self._routing.values()):
            setattr(self, camelcase_to_underscore(service_class.__name__), domain.get_service(service_class))
        
        # Generate the routing
        for method_name, service_class in self._routing.items():
            service = domain.get_service(service_class)
            setattr(self, method_name, getattr(service, method_name))
        
###################
### TIME SERVICE ##
###################
            
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
    
##################
### LOG SERVICE ##
##################
class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
    
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
    
    def flush(self):
        pass


class LoggerService(Service):
    """
    Service that provides logging facilities.
    """
    DEFAULT_LOG_LEVEL = logging.INFO
    DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DEFAULT_LOG_MAX_SIZE = 10485760
    DEFAULT_LOG_BACKUP_COUNT = 5

    def __init__(self, domain) -> None:
        super(LoggerService, self).__init__(domain)
        log_path = domain.get_param("app", "log_file_path")

        if not log_path:
            log_path = domain.get_param("logger", "log_to_file")

        log_to_stdout = domain.get_param("app", "log_to_stdout")
        if log_path and not log_to_stdout:
            # Rotation is being forced, stop writing garbage logs
            # Default 10 Mb
            max_files = domain.get_param("logger", "max_file_count", default=self.DEFAULT_LOG_BACKUP_COUNT)
            # Default 10 Files
            max_size_per_file = domain.get_param("logger", "max_file_size", default=self.DEFAULT_LOG_MAX_SIZE)
            hdlr = RotatingFileHandler(log_path, maxBytes=max_size_per_file, backupCount=max_files)

            log_fmt = domain.get_param("logger", "format", default=self.DEFAULT_LOG_FORMAT)
        else:
            hdlr = logging.StreamHandler(sys.stdout)
            log_fmt = domain.get_param("logger", "format", default=self.DEFAULT_LOG_FORMAT)

        formatter = logging.Formatter(log_fmt)
        hdlr.setFormatter(formatter)
        self.DEFAULT_LOG_LEVEL = domain.get_param("logger", "level", default=self.DEFAULT_LOG_LEVEL)
        self.loggers = {}
        self.default_logger = self.get_logger()
        del self.default_logger.handlers[:]
        self.default_logger.addHandler(hdlr)
        self.LOG_LEVELS = {
            "ERROR": {'logger': self.default_logger.error, "enum": en_evt.EventLevel.elError, "level": logging.ERROR},
            "WARNING": {'logger': self.default_logger.warning, "enum": en_evt.EventLevel.elWarning, "level": logging.WARN},
            "CRITICAL": {'logger': self.default_logger.critical, "enum": en_evt.EventLevel.elCritical, "level": logging.CRITICAL},
            "INFO": {'logger': self.default_logger.info, "enum": en_evt.EventLevel.elInfo, "level": logging.INFO},
            "DEBUG": {'logger': self.default_logger.debug, "enum": en_evt.EventLevel.elDebug1, "level": logging.DEBUG},
            "DEBUG2": {'logger': self.default_logger.debug, "enum": en_evt.EventLevel.elDebug2, "level": logging.DEBUG}
        }
        self.domain = domain
        self.evt_proxy = None
        do_redirect_stdout = domain.get_param("logger", "redirect_stdout", default=False)
        do_redirect_stderr = domain.get_param("logger", "redirect_stderr", default=False)
        if do_redirect_stdout:
            self.redirect_stdout()
        if do_redirect_stderr:
            self.redirect_stderr()
    
    def redirect_stdout(self):
        sys.stdout = StreamToLogger(self.get_logger("stdout"), logging.INFO)

    def redirect_stderr(self):
        sys.stderr = StreamToLogger(self.get_logger("stderr"), logging.ERROR)

    def revert_stderr(self):
        sys.stderr = StreamToLogger(self.get_logger("stderr"), logging.ERROR)

    def revert_stdout(self):
        sys.stderr = sys.__stderr__

    def redirect_streams(self):
        self.redirect_stdout()
        self.redirect_stderr()
    
    def revert_streams(self):
        self.revert_stdout()
        self.revert_stderr()

    def set_log_level(self, level_string, name=None):
        lvl = self.LOG_LEVELS.get(level_string.upper())
        if lvl is None:
            return
        self.get_logger(name).setLevel(lvl["level"])

    def revert_log_level(self, name=None):
        self.get_logger(name).setLevel(self.DEFAULT_LOG_LEVEL)

    def get_logger(self, name=None):
        if name in self.loggers:
            return self.loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(self.DEFAULT_LOG_LEVEL)
        logger.ex2str = LoggerService.ex2str

        def log(msg, level_string='INFO'):
            lvl = self.LOG_LEVELS[level_string]['level']
            logger.__builtin_log__(lvl, msg)
        
        logger.__builtin_log__ = logger.log
        logger.log = log

        self.loggers[name] = logger
        return logger
    
    def log(self, msg, level_string="INFO", broadcast_topic=None, uticker="", ticker=""):
        level_string = level_string.upper()
        if level_string not in self.LOG_LEVELS:
            return
        self.LOG_LEVELS[level_string]['logger'](msg)

        if self.evt_proxy is None:
            from GoldenSource.python.ice.ice_service import IceService
            self.evt_proxy = self.domain.get_service(IceService).get_proxy("events")

        if broadcast_topic and self.evt_proxy is not None:
            ev = do_evt.EventInfo()
            ev.m_level = self.LOG_LEVELS[level_string]['enum']
            ev.m_msg = msg
            ev.m_topic = broadcast_topic
            ev.m_ticker = ticker
            ev.m_underlyingTicker = uticker
            self.evt_proxy.addEvent(ev)
    
    @staticmethod
    def ex2str(extype=None, exvalue=None, extb=None):
        if sys is None:
            return
        
        stype, svalue, strace = sys.exc_info()

        if extype is None:
            extype = stype
        if exvalue is None:
            exvalue = svalue
        if extb is None:
            extb = strace
        return "".join(traceback.format_exception(extype, exvalue, extb))
    
    def __str__(self) -> str:
        return "log_level:{!s} log_format:{!s} log_file:{!s} log_max_size:{!s} log_backup_count:{!s}".format(self._log_level, self._log_format, self._log_file, self._log_max_size, self._log_backup_count)
    
    def __repr__(self) -> str:
        return "LoggerService({!r}, {!r}, {!r}, {!r}, {!r})".format(self._log_level, self._log_format, self._log_file, self._log_max_size, self._log_backup_count)

class NullLoggerService(LoggerService):
    __meta__class = patterns.Singleton

    def __init__(self, domain) -> None:
        pass

    def set_log_level(self, level_string, name=None):
        pass

    def revert_log_level(self, name=None):
        pass

    def get_logger(self, name=None):
        return NullLogger()
    
    def log(self, msg, level_string, broadcast_topic=None, uticker="", ticker=""):
        pass

class NullLogger(object):
    def __init__(self) -> None:
        pass
    
    def _log(self, *args, **kwargs):
        pass

    debug = _log
    info = _log
    warn = _log
    warning = _log
    error = _log
    exception = _log
    log = _log