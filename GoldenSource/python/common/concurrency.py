import contextlib
import multiprocessing
import sys
import time
from datetime import datetime
from threading import Thread, Condition, Lock, Event, RLock
from queue import Queue, Empty
from GoldenSource.python.common.domain import Domain


class CountDownLatch(object):
    """
    A synchronization aid that allows one or more threads to wait until a set of operations being performed in other threads completes
    """

    def __init__(self, count=1):
        """
        Initializes the CountDownLatch with the given count
        :param count: The count
        """
        self.count = count
        self.lock = Condition()

    def count_down(self):
        """
        Decrements the count of the latch, releasing all waiting threads when the count reaches zero
        """
        self.lock.acquire()
        self.count -= 1
        if self.count <= 0:
            self.lock.notify_all()
        self.lock.release()

    def wait(self):
        """
        Causes the current thread to wait until the latch has counted down to zero, unless the thread is interrupted
        :param timeout: The maximum time to wait
        :return: True if the count reached zero, False if the waiting time elapsed before the count reached zero
        """
        self.lock.acquire()
        while self.count > 0:
            self.lock.wait()
        self.lock.release()

class Future(object):
    """
    Future result object returned when queuing a job in a ThreadPool Trying to get the result will hold until the task is completed.
    The status of the call can be monitored using the done and successful flags. In case of an unsuccessful run, the error details can be retrieved
    with error.
    """

    def __init__(self, func, *args, **kwargs):
        # Job information
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._func_str = self._func.__name__ if hasattr(self._func, '__name__') else str(self._func)
        self._args_str = ", ".join(repr(v) for v in self._args) + ", ".join("{}={!r}".format(k, repr(v)) for k, v in self._kwargs.items())

        # Lock to restrict certain accesses
        self._lock = Condition()
        self._reset()

    def _reset(self):
        """
        Resets the future state
        """
        self._result = None
        self._running = False
        self._successful = False
        self._done = False
        self._error = None
        self._exec_time = None

    def __call__(self):
        """
        Calls the inner job all-the-while maintaining all other flags up-to-date
        Note that calling this will effectively be the same as calling the wrapped function with the overhead of setting the internal
        flags and status of the Future object
        """
        try:
            self._reset()

            self._lock.acquire()
            t = time.time()
            self._running = True
            self._result = self._func(*self._args, **self._kwargs)
        except:
            self._successful = False
            self._error = sys.exc_info()
        else:
            self._successful = True
            return self._result
        finally:
            self._exec_time = time.time() - t
            self._done = True
            self._running = False
            self._lock.notify_all()
            self._lock.release()

    def get(self):
        """
        Holds until the job completes, then returns the result if the job completed normally.
        The error or exception that caused the job to fail can be retrieved with the error method
        """
        result = self.result
        if not self.successful:
            raise self.error[0]
        return result

    @property
    def result(self):
        """
        Returns the result of the job if it has completed
        """
        # Block only as long as the job has not completed
        if not self._done:
            self._lock.acquire()
            while not self._done:
                self._lock.wait()
            self._lock.release()
        return self._result
    
    @property
    def successful(self):
        """
        Returns True if the job completed successfully
        """
        return self._successful
    
    @property
    def running(self):
        """
        Returns True if the job is currently running
        """
        return self._running

    @property
    def done(self):
        """
        Returns True if the job has completed
        """
        return self._done
    
    @property
    def error(self):
        """
        Returns the error that caused the job to fail
        """
        return self._error
    
    @property
    def execution_time(self):
        """
        Returns the execution time in seconds.
        None is returned if the job has not yet been invoked nor completed
        """
        return self._exec_time
    
    def __str__(self):
        return "{}({})".format(self._func_str, self._args_str)
    
    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._func_str, self._args_str)

class Worker(Thread):
    """
    Thread executing tasks from a given tasks queue
    """

    def __init__(self, tasks=None, name=None):
        super(Worker, self).__init__(name=name)
        self.stop_request = Event()
        if tasks is not None:
            self.tasks = tasks
        else:
            self.tasks = Queue()
        self.daemon = True
        self.logger_service = Domain().logger_service
        self.logger = self.logger_service.get_logger(Worker.__name__)
        self.start()

    def add_task(self, func, *args, **kwargs):
        """
        Add a task to the queue
        """
        future = Future(func, *args, **kwargs)
        self.tasks.put(future, block=False)
        return future

    def run(self):

        """
        Starts the worker thread. It will run until terminate is called.
        """
        while not self.stop_request.isSet():
            try:
                future = self.tasks.get(block=True, timeout=2)
            except Empty:
                pass
            except:
                self.logger.exception()
            else:
                try:
                    future()
                except:
                    self.logger.exception("Error while executing {!s}".format(future))
                    pass
                finally:
                    self.tasks.task_done()

    def terminate(self):
        """
        Stops the worker thread
        """
        self.stop_request.set()


class Threadpool(list):
    SLOTS_MULT = 100
    """ Pool of threads consuming tasks from a queue """

    def __init__(self, name, num_threads, num_slots=0, blocking=False):
        super(Threadpool, self).__init__()
        self._name = name
        self._blocking = blocking
        if num_slots > 0:
            self.tasks = Queue(num_slots)
        else:
            self.tasks = Queue(num_threads * self.SLOTS_MULT)
        for i in range(num_threads):
            self.append(Worker(self.tasks, name="{}:Thread-{}".format(self._name, i)))

    def add_task(self, func, *args, **kwargs):
        """
        Add a task to the queue
        """
        future = Future(func, *args, **kwargs)
        self.tasks.put(future, block=self._blocking)
        return future

    def wait_completion(self):
        """
        Waits for all tasks to be completed
        """
        self.tasks.join()

    def terminate(self):
        """
        Terminates the threadpool, effectively requesting all worker threads to stop and waiting up to 2 seconds per thread.
        No guarantee is made that the threads will be fully stpped by the time this method returns
        """
        for worker in self:
            worker.terminate()
        for worker in self:
            worker.join(2)

class AllocatingThreadpool(list):
    SLOTS_MULT = 100
    """Pool of threads with tasks allocated to each thread according to abstract allocation logic"""

    def __init__(self, name, num_threads, num_slots_per_thread=0, blocking=False):
        super(AllocatingThreadpool, self).__init__()
        self._name = name
        self._blocking = blocking
        for i in range(num_threads):
            queue = Queue(num_slots_per_thread if num_slots_per_thread > 0 else self.SLOTS_MULT)
            worker = Worker(queue, name="{}:Thread-{}".format(self._name, i))
            self.append(worker)

    def allocate_worker(self, subject):
        raise NotImplementedError("{}.allocate_worker".format(self.__class__.__name__))

    def add_task(self, subject, func, *args, **kwargs):
        """
        Add a task to the queue
        """
        worker = self.allocate_worker(subject)
        return worker.add_task(func, *args, **kwargs)
    
    def wait_completion(self):
        """
        Waits for all tasks to be completed
        """
        for worker in self:
            worker.task.join()
    
    def terminate(self):
        """
        Terminates the threadpool, effectively requesting all worker threads to stop and waiting up to 2 seconds per thread.
        No guarantee is made that the threads will be fully stpped by the time this method returns
        """
        for worker in self:
            worker.terminate()
        for worker in self:
            worker.join(2)

class AssignedThreadpool(AllocatingThreadpool):
    def __init__(self, name, num_threads, num_slots_per_thread=0, blocking=False):
        super(AssignedThreadpool, self).__init__(name, num_threads, num_slots_per_thread, blocking)
        self._worker_by_subject = {}
        self._load_by_worker = {w: 0 for w in self}
        self._lock = RLock()

    def _work_for_subject(self, subject):
        return 1

    def _assign_worker(self, subject, new_work):
        min_load_worker, min_load = None, None
        for worker, load in self._load_by_worker.items():
            if min_load_worker is None or load < min_load:
                min_load_worker, min_load = worker, load
        return min_load_worker

    def allocate_worker(self, subject):
        worker = self._worker_by_subject.get(subject)
        if worker is None:
            with self._lock:
                worker = self._worker_by_subject.get(subject)
                if worker is None:
                    new_work = self._work_for_subject(subject)
                    worker = self._assign_worker(subject, new_work)
                    self._worker_by_subject[subject] = worker
                    self._load_by_worker[worker] += new_work
        return worker

def spawn(f):
    def fun(q_in, q_out):
        while True:
            i, x = q_in.get()
            if i is None:
                break
            q_out.put((i, f(x)))

    return fun


def parmap(f, X, nprocs=multiprocessing.cpu_count()):
    q_in = multiprocessing.Queue(1)
    q_out = multiprocessing.Queue()

    proc = [multiprocessing.Process(target=spawn(f), args=(q_in, q_out)) for _ in range(nprocs)]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]


class Timer(Thread):
    counter = 0

    def __init__(self, event, fcn, interval=1, name=None, immediate=False):
        super(Timer, self).__init__()
        if not name:
            self.name = "Timer-{}".format(Timer.counter)
            Timer.counter += 1
        else:
            self.name = name
        self.immediate = immediate
        self.stopped = event
        self.interval = interval
        self.last_called = None
        self.fcn = fcn
        self.daemon = True
        self.logger_service = Domain().logger_service
        self.logger = self.logger_service.get_logger(self.__class__.__name__)

    def run(self):
        if self.immediate:
            try:
                self.fcn()
            except:
                self.logger.exception("{} failed".format(self.fcn))
            finally:
                self.last_called = datetime.now()
                self.immediate = False

        while not self.stopped.wait(self.interval):
            try:
                self.fcn()
            except:
                self.logger.exception("{} failed".format(self.fcn))
            finally:
                self.last_called = datetime.now()

    def __str__(self):
        return "{}<every {:.4f} seconds>".format(self.name, self.interval)

    def __repr__(self):
        return "{}({!r},{!r},{!r},{!r},{!r})".format(self.__class__.__name__, self.stopped, self.fcn, self.interval, self.name, self.immediate)

class NotifiableTimer(Thread):
    counter = 0

    def __init__(self, condition, fcn, interval=1, name=None, immediate=False):
        super(NotifiableTimer, self).__init__()
        if not name:
            self.name = "Timer-{}".format(Timer.counter)
            Timer.counter += 1
        else:
            self.name = name
        self.immediate = immediate
        self.condition = condition
        self.interval = interval
        self.last_called = None
        self.fcn = fcn
        self.daemon = True
        self.stopped = False
        self.first = True
        self.logger_service = Domain().logger_service
        self.logger = self.logger_service.get_logger(self.__class__.__name__)

    def stop_thread(self):
        self.condition.acquire()
        self.stopped = True
        self.condition.notify()
        self.condition.release()

    def notify_thread(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def run(self):

        self.condition.acquire()
        while not self.stopped:

            if self.first:
                # First time run, check if immediate run is required, otherwise just wait
                self.first = False
                if self.immediate:
                    try:
                        self.fcn()
                    except:
                        self.logger.exception("{} failed".format(self.fcn))
                    finally:
                        self.last_called = datetime.now()
                        self.immediate = False

            else:
                # Since this is not the first run, just call the function and then wait
                try:
                    self.fcn()
                except:
                    self.logger.exception("{} failed".format(self.fcn))
                finally:
                    self.last_called = datetime.now()

            if not self.stopped:
                self.condition.wait(self.interval)

        self.condition.release()

    def __str__(self):
        return "{}<every {:.4f} seconds>".format(self.name, self.interval)

    def __repr__(self):
        return "{}({!r},{!r},{!r},{!r},{!r})".format(self.__class__.__name__
                                                     , self.stopped
                                                     , self.fcn
                                                     , self.interval
                                                     , self.name)


class RWLock(object):
    """Synchronization object used in a solution of so-called second 
    readers-writers problem. In this problem, many readers can simultaneously 
    access a share, and a writer has an exclusive access to this share.
    Additionally, the following constraints should be met: 
    1) no reader should be kept waiting if the share is currently opened for 
        reading unless a writer is also waiting for the share, 
    2) no writer should be kept waiting for the share longer than absolutely 
        necessary. 

    The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7] 
    with a modification -- adding an additional lock (C{self._readers_queue})
    -- in accordance with [2].
        
    Sources:
    [1] A.B. Downey: "The little book of semaphores", Version 2.1.5, 2008
    [2] P.J. Courtois, F. Heymans, D.L. Parnas:
        "Concurrent Control with 'Readers' and 'Writers'", 
        Communications of the ACM, 1971 (via [3])
    [3] http://en.wikipedia.org/wiki/Readers-writers_problem
    """

    def __init__(self):
        self._read_switch = _LightSwitch()
        self._write_switch = _LightSwitch()
        self._no_readers = Lock()
        self._no_writers = Lock()
        self._readers_queue = Lock()
        """A lock giving an even higher priority to the writer in certain
        cases (see [2] for a discussion)"""

    @contextlib.contextmanager
    def read_lock(self):
        try:
            self.reader_acquire()
            yield
        finally:
            self.reader_release()

    @contextlib.contextmanager
    def write_lock(self):
        try:
            self.writer_acquire()
            yield
        finally:
            self.writer_release()

    def reader_acquire(self):
        with self._readers_queue:
            with self._no_readers:
                self._read_switch.acquire(self._no_writers)

    def reader_release(self):
        self._read_switch.release(self._no_writers)

    def writer_acquire(self):
        self._write_switch.acquire(self._no_readers)
        self._no_writers.acquire()

    def writer_release(self):
        self._no_writers.release()
        self._write_switch.release(self._no_readers)
        
class _LightSwitch:
    """An auxiliary "light switch"-like object. The first thread turns on the 
    "switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""
    def __init__(self):
        self.__counter = 0
        self.__mutex = Lock()
    
    def acquire(self, lock):
        with self.__mutex:
            self.__counter += 1
            if self.__counter == 1:
                lock.acquire()

    def release(self, lock):
        with self.__mutex:
            self.__counter -= 1
            if self.__counter == 0:
                lock.release()

class Trigger(object):
    """
    Defines an object which trigger(domain) method is meant to be invoked by the MonirotService when a series of jobs completes
    """

    def trigger(self, domain):
        """
        Method to be invoked by the MonitorService when a series of jobs completes
        :param domain: The domain
        """
        raise NotImplementedError("{}.trigger".format(self.__class__.__name__))
    
    def __str__(self):
        return "{}".format(self.__class__.__name__)
