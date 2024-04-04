
import sys
import traceback
import logging
from logging.handlers import RotatingFileHandler

import GS.enums.event as en_evt
import GS.dataobjects.event as do_evt

from GoldenSource.python.utils import patterns
from GoldenSource.python.common.services import Service



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

class NullLoggerService(LoggerService, metaclass=patterns.Singleton):

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