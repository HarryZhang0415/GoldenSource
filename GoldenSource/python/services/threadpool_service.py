import functools

from GoldenSource.python.utils import patterns
from GoldenSource.python.common.domain import Domain
from GoldenSource.python.common.concurrency import Threadpool
from GoldenSource.python.common.services import Service



class ThreadpoolService(Service, metaclass=patterns.Singleton):
    """
    Threading service, providing a common threading interface to multitasking. Note that this uses threading underneath, not multiprocessing

    https://realpython.com/python-metaclasses/#custom-metaclasses
    
    """
    # __metaclass__ = patterns.Singleton // python 2.7
    DEFAULT_POOL_NAME = "DEFAULT"
    DEFAULT_POOL_SIZE = 5
    _THREAD_COUNT = 'number'
    _QUEUE_SIZE = 'queue'
    _BLOCKING_QUEUE = 'blocking_queue'

    def __init__(self, domain):
        super(ThreadpoolService, self).__init__(domain)
        self._domain = domain
        self._default_thread_count = domain.get_param('threading', self._THREAD_COUNT, default=self.DEFAULT_POOL_SIZE)
        self._default_queue_size = domain.get_param('threading', self._QUEUE_SIZE, default=0)
        self._default_blocking_queue = domain.get_param('threading', self._BLOCKING_QUEUE, default=False)
        self._pools = {}

    def __getitem__(self, name):
        return self.get_pool(name)

    def get_pool(self, name=DEFAULT_POOL_NAME, **kwargs):
        if name not in self._pools:
            thread_count = kwargs.get(
                self._THREAD_COUNT
                , self._domain.get_param('threading', name, self._THREAD_COUNT, default=self._default_thread_count)
            )
            queue_size = kwargs.get(
                self._QUEUE_SIZE
                , self._domain.get_param('threading', name, self._QUEUE_SIZE, default=self._default_queue_size)
            )
            blocking_queue = kwargs.get(
                self._BLOCKING_QUEUE
                , self._domain.get_param('threading', name, self._BLOCKING_QUEUE, default=self._default_blocking_queue)
            )
            self._pools[name] = Threadpool(name, thread_count, queue_size, blocking=blocking_queue)
        return self._pools[name]

    def wait_completion(self):
        for pool in self._pools.values():
            pool.wait_completion()

    def shutdown(self):
        for pool in self._pools.values():
            pool.terminate()


class Threadify(object):
    """
    Convenient decorator to implicitly call a given function or method on a given threadpool. Uses the ThreadPoolService under the hood
    The wrapped function will return a Future.
    """

    def __init__(self, pool_name=ThreadpoolService.DEFAULT_POOL_NAME):
        self.pool_name = pool_name

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pool = Domain().get_service(ThreadpoolService).get_pool(self.pool_name)
            return pool.add_task(func, *args, **kwargs)

        return wrapper