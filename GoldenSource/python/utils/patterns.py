import functools
import time
from GoldenSource.python.error.parse import BadConfigException

class Singleton(type):
    """
    Singleton type is a metaclass enforcing the children classes instances are unique during runtime
    Use cases: 
    class MyClass(BaseClass, metaclass=Singleton):
        pass
    """
    _instances = {}

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwds)
        return cls._instances[cls]
    
def cache_result(wrapped_func):
    @functools.wraps(wrapped_func)
    def wrapper_func(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        res = wrapper_func.__results_cache.get(key)
        if res is None:
            res = wrapper_func.__results_cache[key] = wrapped_func(*args, **kwargs)
        return res
    
    wrapper_func.__results_cache = {}

    def reset_cache():
        wrapper_func.__results_cache = {}
    
    wrapper_func.reset_cache = reset_cache

    return wrapper_func

class ReadOnlyDescriptor(object):
    """
    Read-only attribute descriptor that binds instance._attr to instance.attr
    This prevents any reading to occur from any attribute as long as the underlying attribute has not been set by the instance
    Trying to set the attribute generates a Value Error
    """

    def __init__(self, attr_name, ex_type=BadConfigException) -> None:
        self.attr_name = attr_name
        self._attr_name = "_" + attr_name
        self.ex_type = ex_type

    def __get__(self, instance, owner):
        if not hasattr(instance, self._attr_name):
            raise self.ex_type("{attr} unavailable, {module}.{cls}.{method} needs to be called explicitely".format(attr = self.attr_name, 
                                                                                                                   module = instance.__module__,
                                                                                                                   cls = owner.__name__,
                                                                                                                   method = instance.parse.__name__))
        return getattr(instance, self._attr_name)

    def __set__(self, instance, value):
        raise ValueError("{} is read-only".format(self.attr_name))


class TimeIt(object):
    """
    Times the execution of a code block
    : param on_enter: 0 argument callable to call before entering the block
    : param on_exit: 1 argument callable to call before exiting the block
    : param logger: logger class to use
    : param tag: logger tag to print in lag statement

    To log a block one can provide:
    A) An on_enter and/or on_exit callable(s)
    B) A logger object
    C) A tag

    Precedence rule:
    1) If either (or both) on_enter and on_exit are provided, they supercede all other arguments
    2) If no callable is provided, the default functions are used
    3) If no logger is provided, the log is printed using print()
    4) If no tag is provided, nothing will be logged

    Example:
    >>> with timeIt(
    ...     on_enter=lambda: self.logger.info('Starting operation),
    ...     on_exit=lambda t: self.logger.info('Operation completed in {:.6f} seconds'.format(t))
    ...):
    ...     # <code block>
    ...     pass
    Output:
        Starting operation
        Operation completed in 0.000008 seconds


    >>> with timeIt(
    ...     logger=domain.logger_service.default_logger,
    ...     tag = 'Operation DoThatThing'
    ...):
    ...     # <code block>
    ...     pass
    Output:
        Starting <Operation DoThatThing>
        <Operation DoThatThing> took 0.000008 seconds

    >>> with timeIt() as timeit:
    ...     # <code block>
    ...     pass
    >>> timeit.time_elapsed
    Output:
        8.106e-06
    """

    def __init__(self, on_enter=None, on_exit=None, logger=None, tag=None, level='INFO') -> None:
        self._on_enter = on_enter
        self._on_exit = on_exit
        self._logger = logger
        self._tag = tag
        self._level = None
        self._time = None

        if self._on_enter:
            assert callable(self._on_enter), 'on_enter must be callable'
            assert self._on_enter.__code__.co_argcount == 0, 'on_enter must have 0 arguments'
        if self._on_exit:
            assert callable(self._on_exit), 'on_exit must be callable'
            assert self._on_exit.__code__.co_argcount == 1, 'on_exit must have 1 argument'
        
        if not (self._on_enter or self._on_exit) and self._tag is not None:
            assert isinstance(level, str), 'level must be a string'
            self._level = level.upper()

            if self._logger:
                self._on_enter = self.default_enter
                self._on_exit = self.default_exit
            else:
                self._on_enter = self.print_enter
                self._on_exit = self.print_exit
        
    def default_enter(self):
        self._logger.log('Starting <{}>'.format(self._tag), level_string=self._level)

    def default_exit(self, t):
        self._logger.log('<{}> took {:.6f} seconds'.format(self._tag, t), level_string=self._level)

    def print_enter(self):
        print('Starting <{}>'.format(self._tag))

    def print_exit(self, t):
        print('<{}> took {:.6f} seconds'.format(self._tag, t))

    @property
    def time_elapsed(self):
        return self._time
    
    def __enter__(self):
        if self._on_enter:
            self._on_enter()
        self._time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._time = time.time() - self._time
        if exc_type is not None:
            return False
        if self._on_exit:
            self._on_exit(self._time)
        return True