from queue import Full
import copy
from functools import partial
import threading
import time
import unittest 
import os

from GoldenSource.common.services import NullLoggerService
from GoldenSource.common.concurrency import ThreadpoolService, MonitorService, Trigger, Threadify, RWLock
from GoldenSource.common.domain import Domain
from GoldenSource.common.config import LocalConfigurator

class TestConfigurator(LocalConfigurator):
    def parse(self, args=None, fail_on_err=False):
        args = ['--home-path', os.environ.get("PROJECT_BUILD_DIR")]
        return super(TestConfigurator, self).parse(args, fail_on_err)

@unittest.skip("Not Working With unittest discover")
class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threading = Domain(TestConfigurator).get_service(ThreadpoolService)

    @classmethod
    def tearDownClass(cls):
        Domain(TestConfigurator).shutdown()

    def setUp(self):
        self.pool = self.threading.get_pool()

    def raise_error(self, ex_type):
        time.sleep(1)
        raise ex_type("error")
    
    def set_with_delay(self, k, v):
        """
        Test function class. Will assign v to k in the values dictionary afer a 1-second delay.
        Meant to be called in a separate thread to illustrate the threading behaviors.
        """
        time.sleep(1)
        self.values[k] = v
        return v
    
    @Threadify()
    def parallel_set_with_delay(self, k, v):
        """
        Test function class. Will assign v to k in the values dictionary afer a 1-second delay.
        Meant to be called in a separate thread to illustrate the threading behaviors.
        Note the suntax of the decorator with optional pool name to use as an argument.
        """
        time.sleep(1)
        self.values[k] = v
        return v

    def test_pool_error(self):
        self.pool.add_task(self.raise_error, k="val1", v=1)
        self.pool.add_task(self.raise_error, k="val2", v=2)

        self.pool.wait_completion()

    def test_pool(self):
        self.values = {}

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        self.pool.add_task(self.set_with_delay, k="val1", v=1)
        self.pool.add_task(self.set_with_delay, k="val2", v=2)

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        self.pool.wait_completion()

        self.assertEqual(self.values, {"val1": 1, "val2": 2})

    @unittest.skip("Not working as expected")
    def test_threadify(self):
        self.values = {}

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        self.parallel_set_with_delay("val1", 1)
        self.parallel_set_with_delay("val2", 2)

        # self.assertIsNone(self.values.get("val1"))
        # self.assertIsNone(self.values.get("val2"))

        self.pool.wait_completion()

        # time.sleep(3)

        self.assertEqual(self.values.get("val1"), 1)
        self.assertEqual(self.values.get("val2"), 2)

    def test_successful_future(self):
        self.values = {}

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        fut1 = self.pool.add_task(self.set_with_delay, k="val1", v=1)
        fut2 = self.pool.add_task(self.set_with_delay, k="val2", v=2)

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        # Verify all properties pre-execution
        self.assertFalse(fut1.done)
        self.assertFalse(fut1.successful)
        self.assertIsNone(fut1.error)
        self.assertFalse(fut2.done)
        self.assertFalse(fut2.successful)
        self.assertIsNone(fut2.error)

        # Execution holds on retrieving futX.result
        self.assertEqual(fut2.result, self.values.get("val2"))
        self.assertEqual(fut1.get(), self.values.get("val1"))
        self.assertEqual(fut1.result, self.values.get("val1"))
        self.assertEqual(fut2.get(), self.values.get("val2"))

        # Verify all properties post-execution
        self.assertTrue(fut1.done)
        self.assertTrue(fut1.successful)
        self.assertIsNone(fut1.error)
        self.assertTrue(fut2.done)
        self.assertTrue(fut2.successful)
        self.assertIsNone(fut2.error)

    def test_unsuccessful_future(self):
        self.values = {}

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        fut1 = self.pool.add_task(self.raise_error, ex_type=ValueError)
        fut2 = self.pool.add_task(self.raise_error, ex_type=NotImplementedError)

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        self.assertFalse(fut1.done)
        self.assertFalse(fut1.successful)
        self.assertIsNone(fut1.error)
        self.assertFalse(fut2.done)
        self.assertFalse(fut2.successful)
        self.assertIsNone(fut2.error)

        # Execution holds on retrieving futX.result
        self.assertIsNone(fut1.result)
        self.assertRaises(ValueError, fut1.get)
        self.assertIsNone(fut2.result)
        self.assertRaises(NotImplementedError, fut2.get)

        # Verify all properties post-execution
        self.assertTrue(fut1.done)
        self.assertFalse(fut1.successful)
        self.assertEqual(fut1.error[0], ValueError)
        self.assertTrue(fut2.done)
        self.assertFalse(fut2.successful)
        self.assertEqual(fut2.error[0], NotImplementedError)

    def test_filling_blocking_queue(self):
        self.values = {}

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        for i in range(10):
            self.pool.add_task(self.set_with_delay, k=f"val{i}", v=i)

        self.assertIsNone(self.values.get("val1"))
        self.assertIsNone(self.values.get("val2"))

        self.pool.wait_completion()

        self.assertEqual(self.values, {f"val{i}": i for i in range(10)})
        non_blocking_pool = self.threading.get_pool('test_filling_blcking_queue:pool', number=1, queue=1, blocking_queue=False)
        try:
            for i in range(10):
                non_blocking_pool.add_task(self.set_with_delay, 'test_filling_blocking_queue:value', v=i)
        except Exception as e:
            self.assertIsInstance(e, Full)
        else:
            self.assertTrue(False, "Queue.Full should have been raised")
    
    def test_filling_non_blocking_queue(self):
        self.values = {}
        non_blocking_pool = self.threading.get_pool('test_filling_non_blocking_queue:pool', number=1, queue=1, blocking_queue=True)
        for i in range(10):
            non_blocking_pool.add_task(self.set_with_delay, 'test_filling_non_blocking_queue:value', v=i)
        non_blocking_pool.wait_completion()
        self.assertEqual(i, self.values['test_filling_non_blocking_queue:value'])

class Writer(threading.Thread):
    def __init__(self, buffer_, rw_lock, init_sleep_time, sleep_time, to_write):
        """
        @param buffer_: common buffer_ shared by the readers and writers
        @type buffer_: List
        @type rw_lock: RWLock
        @param init_sleep_time: initial sleep time before writing
        @type init_sleep_time: float
        @param sleep_time: sleep time while in critical section
        @type sleep_time: float
        @param to_write: value to write to the buffer_
        """       
        threading.Thread.__init__(self)
        self._buffer = buffer_
        self._rw_lock = rw_lock
        self._init_sleep_time = init_sleep_time
        self._sleep_time = sleep_time
        self._to_write = to_write
        self.entry_time = None
        """Time of entry to the critical section"""
        self.exit_time = None
        """Time of exit from the critical section"""

    def run(self):
        time.sleep(self._init_sleep_time)
        self._rw_lock.writer_acquire()
        self.entry_time = time.time()
        time.sleep(self._sleep_time)
        self._buffer.append(self._to_write)
        self.exit_time = time.time()
        self._rw_lock.writer_release()


class Reader(threading.Thread):
    def __init__(self, buffer_, rw_lock, init_sleep_time, sleep_time):
        """
        @param buffer_: common buffer_ shared by the readers and writers
        @type buffer_: List
        @type rw_lock: RWLock
        @param init_sleep_time: initial sleep time before reading
        @type init_sleep_time: float
        @param sleep_time: sleep time while in critical section
        @type sleep_time: float
        """       
        threading.Thread.__init__(self)
        self._buffer = buffer_
        self._rw_lock = rw_lock
        self._init_sleep_time = init_sleep_time
        self._sleep_time = sleep_time
        self.buffer_read = None
        """a copy of buffer read while in critical section"""
        self.entry_time = None
        """Time of entry to the critical section"""
        self.exit_time = None
        """Time of exit from the critical section"""

    def run(self):
        time.sleep(self._init_sleep_time)
        self._rw_lock.reader_acquire()
        self.entry_time = time.time()
        time.sleep(self._sleep_time)
        self.buffer_read = copy.deepcopy(self._buffer)
        self.exit_time = time.time()
        self._rw_lock.reader_release()

@unittest.skip("Not Working With unittest discover")
class RWLockTestCase(unittest.TestCase):
    def test_readers_nonexclusive_access(self):
        (buffer_, rw_lock, threads) = self._init_variables()

        threads.append(Reader(buffer_, rw_lock, 0, 0))
        threads.append(Writer(buffer_, rw_lock, 0.2, 0.4, 1))
        threads.append(Reader(buffer_, rw_lock, 0.3, 0.3))
        threads.append(Reader(buffer_, rw_lock, 0.5, 0))

        self._start_and_join_threads(threads)

        ## The thrid reader should enter after the second one but it should 
        ## exit before the second one exits
        ## (i.e. the readers should be in the critical section at the same time)

        self.assertEqual([], threads[0].buffer_read)
        self.assertEqual([1], threads[2].buffer_read)
        self.assertEqual([1], threads[3].buffer_read)
        self.assertTrue(threads[1].exit_time <= threads[2].entry_time)
        self.assertTrue(threads[2].entry_time <= threads[3].entry_time)
        self.assertTrue(threads[3].exit_time <= threads[2].exit_time)

    def test_writer_exclusive_access(self):
        (buffer_, rw_lock, threads) = self._init_variables()

        threads.append(Writer(buffer_, rw_lock, 0, 0.4, 1))
        threads.append(Writer(buffer_, rw_lock, 0.1, 0, 2))
        threads.append(Reader(buffer_, rw_lock, 0.2, 0))

        self._start_and_join_threads(threads)

        ## The second writer should enter after the first one but it should 
        ## exit before the first one exits
        ## (i.e. the writers should be in the critical section at the same time)

        self.assertEqual([1, 2], threads[2].buffer_read)
        self.assertTrue(threads[0].exit_time <= threads[1].entry_time)
        self.assertTrue(threads[1].exit_time <= threads[2].exit_time)

    def test_writer_priority(self):
        (buffer_, rw_lock, threads) = self._init_variables()

        threads.append(Writer(buffer_, rw_lock, 0, 0, 1))
        threads.append(Reader(buffer_, rw_lock, 0.1, 0.4))
        threads.append(Writer(buffer_, rw_lock, 0.2, 0, 2))
        threads.append(Reader(buffer_, rw_lock, 0.3, 0))
        threads.append(Reader(buffer_, rw_lock, 0.3, 0))

        self._start_and_join_threads(threads)

        ## The second writer should enter after the first one but it should 
        ## exit before the first one exits
        ## (i.e. the writers should be in the critical section at the same time)

        self.assertEqual([1], threads[1].buffer_read)
        self.assertEqual([1,2], threads[3].buffer_read)
        self.assertEqual([1,2], threads[4].buffer_read)
        self.assertTrue(threads[0].exit_time <= threads[1].entry_time)
        self.assertTrue(threads[1].exit_time <= threads[2].entry_time)
        self.assertTrue(threads[2].exit_time <= threads[3].entry_time)
        self.assertTrue(threads[2].exit_time <= threads[4].entry_time)

    def test_many_writers_priority(self):
        (buffer_, rw_lock, threads) = self._init_variables()

        threads.append(Writer(buffer_, rw_lock, 0, 0, 1))
        threads.append(Reader(buffer_, rw_lock, 0.1, 0.6))
        threads.append(Writer(buffer_, rw_lock, 0.2, 0.1, 2))
        threads.append(Reader(buffer_, rw_lock, 0.3, 0))
        threads.append(Reader(buffer_, rw_lock, 0.4, 0))
        threads.append(Writer(buffer_, rw_lock, 0.5, 0.1, 3))

        self._start_and_join_threads(threads)

        ## The readers should be in the critical section at the same time
        ## The writers should be in the critical section at the same time

        self.assertEqual([1], threads[1].buffer_read)
        self.assertEqual([1,2,3], threads[3].buffer_read)
        self.assertEqual([1,2,3], threads[4].buffer_read)
        self.assertTrue(threads[0].exit_time <= threads[1].entry_time)
        self.assertTrue(threads[1].exit_time <= threads[2].entry_time)
        self.assertTrue(threads[1].exit_time <= threads[5].entry_time)
        self.assertTrue(threads[2].exit_time <= threads[3].entry_time)
        self.assertTrue(threads[2].exit_time <= threads[4].entry_time)
        self.assertTrue(threads[5].exit_time <= threads[3].entry_time)
        self.assertTrue(threads[5].exit_time <= threads[4].entry_time)

    @staticmethod
    def _init_variables():
        buffer_ = []
        rw_lock = RWLock()
        threads = []
        return (buffer_, rw_lock, threads)
    
    @staticmethod
    def _start_and_join_threads(threads):
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

class Job(object):
    def __init__(self, domain, monitor_id, target):
        self._mon_svc = domain.get_service(MonitorService)
        self._monitor_id = monitor_id
        self._target = target
        self._mon_svc.monitor(self._monitor_id, self)

    def do(self):
        try:
            self._target()
        except:
            pass
        finally:
            self._mon_svc.job_done(self._monitor_id, self)

class TestTrigger(Trigger):
    def __init__(self, obj) -> None:
        super(TestTrigger, self).__init__()
        self._obj = obj

    def trigger(self, domain):
        self._obj.success = True
    
@unittest.skip("Not Working With unittest discover")
class MonitorServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super(MonitorServiceTestCase, self).setUp()
        self.domain = Domain(LocalConfigurator)
        self.thp_svc = self.domain.get_service(ThreadpoolService)
        self.mon_svc = self.domain.get_service(MonitorService)
        self.success = False
    
    def test_monitor(self):
        target = partial(time.sleep, 3)
        monitor_id = "test"
        self.mon_svc.add_trigger(monitor_id, TestTrigger(self))
        jobs = (
            Job(self.domain, monitor_id, target),
            Job(self.domain, monitor_id, target),
            Job(self.domain, monitor_id, target),
        )
        pool = self.thp_svc.get_pool(self.__class__.__name__)
        for job in jobs:
            pool.add_task(job.do)
        
        pool.wait_completion()
        self.assertTrue(self.success, "Monitor trigger not received")

if __name__ == "__main__":
    unittest.main()
    