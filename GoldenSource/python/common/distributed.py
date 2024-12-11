import datetime
import math
import os
import time
import pytz
from collections import defaultdict
from threading import Event, RLock
from functools import reduce

import Ice
from Ice import Identity
from GS.dataobjects import OnDemandAllocation
from GS.exceptions import ValidateException
from GS.interfaces import Allocator as IceAllocator, AllocatorPrx, OnDemandAllocator as IceOnDemandAllocator

from GoldenSource.python.common.concurrency import Timer, ThreadpoolService
from GoldenSource.python.ice.ice_service import IceService, ListenerProxyCache
from GoldenSource.python.ice.servant import AMDContext, IceServant
# from GoldenSource.infra import TidalService
from GoldenSource.python.utils.patterns import TimeIt
from GoldenSource.python.monitoring.heartbeat_service import HeartBeatMonitoringService
import time

__author__ = "hzhang"

class NoAllocationException(Exception):
    def __init__(self, message):
        super(NoAllocationException, self).__init__(message)

class NodeTask(object):
    """
    Generic task for a node. Computes its own cost of execution.

    TOTAL_COST = DEFAULT_COST * DEFAULT_FACTOR + DEFAULT_WEIGHT

    Can be weighted by the identifier of the task:
    TOTAL_COST = COST_MAP[self.identifier] * FACTOR_MAP[self.identifier] + WEIGHT_MAP[self.identifier]

    Can include cost floor by using MIN_COST:
    TOTAL_COST = TOTAL_COST if TOTAL_COST > 0 else MIN_COST
    """
    DEFAULT_COST = 1.  # default base cost of this task
    DEFAULT_FACTOR = 1.  # default factor (multiplicative scaling)
    DEFAULT_WEIGHT = 0.  # default weight (additive bias)
    MIN_COST = 0.1  # minimum computation cost

    def __init__(self, domain, identifier):
        super(NodeTask, self).__init__()
        self.logger_service = domain.logger_service
        self.logger = self.logger_service.get_logger(self.__class__.__name__)

        self._identifier = identifier
        self._cost = 0.

    @property
    def identifier(self):
        return self._identifier

    @property
    def cost(self):
        return self._cost

    def compute_cost(self):
        """
        Compute the cost of running this task.
        :return: Nothing. Mutates self.cost.
        """
        cost = self.DEFAULT_COST * self.DEFAULT_FACTOR + self.DEFAULT_WEIGHT
        self._cost = cost if cost > 0 else self.MIN_COST

    def __hash__(self):
        return hash(self.identifier)

    def __cmp__(self, other):
        if self.identifier > other.identifier:
            return 1
        elif self.identifier < other.identifier:
            return -1
        else:
            return 0

    def __str__(self):
        return '{}(id=<{}>, work={:>4.2f})'.format(
                self.__class__.__name__,
                self.identifier,
                self.cost
        )

    def __repr__(self):
        return self.__str__()


class AllocatorServant(IceAllocator, IceServant):
    # region Allocator settings
    DEFAULT_NODE_COUNT = 0
    DEFAULT_NODE_TIMEOUT = None
    DEFAULT_NODE_BASE_NAME = None
    DEFAULT_NODE_CONFIG = None
    DEFAULT_NODE_LOCATION = None
    DEFAULT_NODE_SCRIPT = None
    DEFAULT_ALLOCATION_CLASS = None

    # endregion

    def __init__(self, domain):
        IceAllocator.__init__(self)
        IceServant.__init__(self, domain)

        self._event = Event()

        self._node_watch = {}
        # will be used to track the nodes that have been spawned once
        self._node_spawn_watch = {}

        self._no_spawn = domain.get_param('app', 'no_spawn', default=False)
        # controls whether re spawning is allowed in case if nodes timeout
        self._no_re_spawn = domain.get_param('app', 'no_re_spawn', default=True)

        self._node_count = self.domain.get_param('app', 'node_count', default=self.DEFAULT_NODE_COUNT)
        assert self._node_count > 0, 'app.node_count parameter is mandatory'
        self._scale = int(math.log10(self._node_count)) + 1

        self._node_timeout = self.domain.get_param('app', 'node_timeout',
                                                   default=self.DEFAULT_NODE_TIMEOUT)
        self._node_base_name = self.domain.get_param('app', 'node_base_name',
                                                     default=self.DEFAULT_NODE_BASE_NAME)
        assert self._node_base_name, 'app.node_config parameter is mandatory'
        default_node_config = self.DEFAULT_NODE_CONFIG
        if default_node_config is None:
            default_node_config = os.path.join(domain.configuration.config_path,
                                               '{}.cfg'.format(self._node_base_name))
        self._node_config = self.domain.get_param('app', 'node_config', default=default_node_config)
        assert self._node_config, 'app.node_config parameter is mandatory'

        self._node_command_line = self.domain.get_param('app', 'node_command_line')

        self._node_location = self.domain.get_param('app', 'node_location', default=self.DEFAULT_NODE_LOCATION)
        if self._node_location is None:
            self.logger.warning('No node location specified!')

        self._node_script = self.domain.get_param('app', 'node_script', default=self.DEFAULT_NODE_SCRIPT)

        # self._tidal = domain.get_service(TidalService)
        self._tidal_job_ids = self.domain.get_param('app', 'tidal_job_ids')
        assert self._tidal_job_ids, 'app.tidal_job_ids parameter is mandatory'

        self._allocation_clazz = self.domain.get_param('app', 'allocation_class',
                                                       default=self.DEFAULT_ALLOCATION_CLASS)
        assert self._allocation_clazz, 'app.allocation_class parameter is mandatory'

        self._allocations = {}  # allocations assigned to each node
        self._node_tasks = defaultdict(set)  # look-up table of tasks assigned to each node
        self._node_load = defaultdict(float)  # total work-load on each node
        self.heartbeat_service = self.domain.get_service(HeartBeatMonitoringService)
        self._all_nodes_ready = False
        if self._no_spawn:
            self.logger.info('Node Spawn is disabled. Nodes wont be started')
        else:
            self.logger.info("Node Spawn is enabled, they will be started later")

        self._tasks = {}

    def _get_tasks(self):
        """
        Generate a list of tasks for the allocator
        :return: list(NodeTask) sorted by descending cost
        """
        raise NotImplementedError('{}._get_tasks'.format(self.__class__.__name__))

    def _add_task(self, allocation, task):
        """
        Add a task to an allocation
        :param allocation: Allocation to add to
        :param task: Task to add
        :return: Nothing. Mutates allocation argument.
        """
        raise NotImplementedError('{}._add_tasks'.format(self.__class__.__name__))

    def _build_allocation_map(self):
        return defaultdict(self._allocation_clazz)

    def _allocate(self):
        """
        Create allocation for each node to fetch.
        Default implementation evenly distributes load across all nodes.
        :return: Nothing. Mutates self._allocations.
        """
        with TimeIt(logger=self.logger):
            tasks = self._get_tasks()
            self.logger.info('{} tasks received.'.format(len(tasks)))
            old_tasks = reduce(lambda x, y: x | y, self._node_tasks.values(), set())
            self.logger.info('{} tasks in lookup table.'.format(len(old_tasks)))
            new_tasks = sorted(tasks - old_tasks, key=lambda t: t.cost)
            self.logger.info('{} new tasks'.format(len(new_tasks)))

            avg_load = sum(task.cost for task in tasks) / self._node_count
            node_range = range(self._node_count)
            allocations = self._build_allocation_map()

            # Add tasks stored in look-up table
            for node_index, stored_tasks in self._node_tasks.items():
                identifier = self._get_identifier(node_index)
                allocation = allocations[identifier]
                for task in stored_tasks:
                    self._add_task(allocation, task)

            # Add new tasks
            while new_tasks:
                if len(node_range) > 1:
                    node_range = [node for node in node_range if self._node_load[node] < avg_load]
                for node_index in node_range:
                    if not new_tasks:
                        break
                    identifier = self._get_identifier(node_index)
                    allocation = allocations[identifier]

                    task = new_tasks.pop()
                    self._add_task(allocation, task)
                    self.logger.info('NEW {} -> {}'.format(task, identifier))
                    self._node_load[node_index] += task.cost
                    self._node_tasks[node_index].add(task)  # store in look-up table

            # Hot swap the allocations map
            self._allocations = allocations
        for node_index, load in self._node_load.items():
            self.logger.info('{} has load {:.2f}'.format(self._get_identifier(node_index), load))

    def ice_init(self):
        # Prepare allocations
        self._allocate()

        # Start the reallocation thread
        interval = self.domain.get_param('app', 'reallocation_interval', default=120)
        reallocation_timer = Timer(self._event, self._allocate, interval)
        reallocation_timer.start()

        # Start the administration thread
        admin_interval = self.domain.get_param('app', 'admin_interval', default=5)
        admin_timer = Timer(self._event, self._administrate_nodes, admin_interval)
        admin_timer.start()
        self.logger.info('{} ready'.format(self.app_name))

    def ice_shutdown(self):
        self._event.set()
        self.logger.info('{} shutting down'.format(self.app_name))

    def _get_instance_id(self, i):
        return '{{:0>{}}}'.format(self._scale).format(i)

    def _get_identifier(self, i):
        return '{}.{}'.format(self._node_base_name, self._get_instance_id(i))

    def _node_heartbeat(self, identifier):
        self._node_watch[identifier] = time.time()
        if identifier not in self._node_watch:
            self.logger.warn('Registered new node {}'.format(identifier))

    def _spawn_node(self, i):

        launcher_args = []
        if self._node_location:
            launcher_args.append('-l {}'.format(self._node_location))
        if self._node_script:
            launcher_args.append('-s {}'.format(self._node_script))

        node_argument = '-- --name="{name}" --instance-name="{instance_name}" --config-file="{config}" {command}'.format(
            name=self._node_base_name,
            instance_name=self._get_instance_id(i),
            config=self._node_config,
            command=self._node_command_line)

        # Prepend the launcher arguments
        if launcher_args:
            node_argument = '{} {}'.format(' '.join(launcher_args), node_argument)

        for _ in range(len(self._tidal_job_ids)):
            # Rotate the job ids
            job_id = self._tidal_job_ids.pop()
            self._tidal_job_ids.insert(0, job_id)

            # The try spawning it
            identifier = self._get_identifier(i)
            if self._tidal.add_job_in_queue(job_id, node_argument):
                self.logger.info('Spawned node {}:{} with arguments [{}]'.format(
                    identifier, job_id, node_argument))
                self._node_watch[identifier] = time.time()

                # Node process has been started, this allocator is no longer responsible for managing this process
                # If there was a tidal error then we expect to restart the allocator, the below true flag will indicate
                # that the process was once started
                self._node_spawn_watch[i] = True
                break
            else:
                self.logger.warn('Failed to spawn node {}:{} with arguments [{}]'.format(
                    identifier, job_id, node_argument))
                self._node_spawn_watch[i] = False

    def _one_node_timeout(self, identifier):
        # The node timed out, take it out
        self.logger.info('{} timed out'.format(identifier))

    def _administrate_nodes(self):

        self.logger.debug('Starting node administration')
        now = time.time()

        nodes_ready = True
        for i in range(self._node_count):
            identifier = self._get_identifier(i)
            last_heartbeat = self._node_watch.get(identifier)
            if last_heartbeat is not None:
                # The node showed some signs of life at some point
                elapsed = now - last_heartbeat
                if self._node_timeout is None or elapsed < self._node_timeout:
                    # We want to monitor the nodes, and the current one is well alive
                    continue
                self._one_node_timeout(identifier)

            # There is a problem with this node, not all nodes are available at this point so we make a note of it
            nodes_ready = False

            if not self._no_spawn:
                # Node spawn is enabled, try to start this node
                # Spawn this node only if it hasn't been spawned yet, or re-spawning is enabled
                if i in self._node_spawn_watch and self._node_spawn_watch[i]:
                    # node was once started
                    if self._no_re_spawn:
                        self.logger.info('Re spawn is disabled, not starting node {} again'.format(i))
                    else:
                        # allowed to restart nodes
                        self._spawn_node(i)
                else:
                    # First time, starting this node
                    self._spawn_node(i)

        self.logger.debug('Completed node administration')
        if nodes_ready != self._all_nodes_ready:
            # status changed from last time
            self._all_nodes_ready = nodes_ready
            if nodes_ready:
                self.logger.info('All nodes are ready, Starting heartbeat for {}'.format(self._node_base_name))
                self.heartbeat_service.add_process_to_heartbeat(self._node_base_name)
            else:
                self.logger.error('Some nodes are erroneous, Stopping heartbeat for {}'.format(self._node_base_name))
                self.heartbeat_service.remove_process_from_heartbeat(self._node_base_name)

    def _get_all_allocations(self):
        self.logger.warn('Unimplemented get_all_allocations functionality, so will be returning an empty list')
        return self._allocation_clazz()

    def getAllocation(self, identifier, current=None):
        cxt = AMDContext('getAllocation|{}'.format(identifier))
        with cxt:
            allocation = self._allocations.get(identifier)
            if allocation is None:
                raise Exception('No allocation found for {}'.format(identifier))

            cxt.ice_return = allocation
        return cxt.future

    def getAllAllocation(self, current=None):
        cxt = AMDContext('getAllAllocation')
        with cxt:
            allocation = self._get_all_allocations()
            if allocation is None:
                raise Exception('There are 0 allocations in cache, something must be broken!')
            cxt.ice_return = allocation
        return cxt.future

    def register(self, identifier, current=None):
        cxt = AMDContext('register|{}'.format(identifier), error_only=True)
        with cxt:
            self._node_heartbeat(identifier)
            cxt.ice_return = None
        return cxt.future


class OnDemandAllocatorServant(IceOnDemandAllocator, AllocatorServant):
    # region Allocator settings
    DEFAULT_ALLOCATION_CLASS = OnDemandAllocation

    # endregion
    # region OnDemandAllocator settings
    UNIVERSE_ELEMENT_TYPES = tuple()

    # endregion

    # region Monitors & Handlers
    class UniverseMonitor(object):
        """
        Administrate the universe of elements to process by the OnDemandAllocator.
        """

        def __init__(self, domain):
            self._logger = domain.logger_service.get_logger(self.__class__.__name__)
            self._universe_lock = RLock()
            self._universe = defaultdict(dict)

        @property
        def universe(self):
            """
            Returns: The current universe of elements to process. The returned structure is safe to modify,
            but *not* the elements themselves.
            """
            with self._universe_lock:
                return self._universe.keys()

        def administrate(self, timeout):
            """
            This method checks if elements of the currently allocated universe can be removed.
            The rules for deciding this are as follows:
            1) if a subscriber to an element has been idle for more than app.element_timeout, remove the client
            2) if an element only has timed out subscribers, remove the element from the universe
            """
            with self._universe_lock:
                cutoff_time = datetime.datetime.now(tz=pytz.UTC) - timeout
                to_drop = set()
                for element, identifiers in self._universe.items():
                    identifiers_alive = {}
                    for identifier, last_seen in identifiers.items():
                        if last_seen > cutoff_time:
                            identifiers_alive[identifier] = last_seen

                    if identifiers_alive:
                        self._universe[element] = identifiers_alive
                    else:
                        self._logger.info('Removing {}, timed out'.format(element))
                        to_drop.add(element)

                for element in to_drop:
                    del self._universe[element]

        def add(self, identifier, elements):
            """
            Adds elements to the universe, monitored by identifier. Every time this method is called for a
            (element, identifier) tuple, the timestamp attached is updated to reflect an active monitoring
            activity from the identifier.

            Args:
                elements: The elements to add active monitoring for
                identifier: The identifier monitoring the elements

            Returns: True if the universe is mutated, ie if new elements have been added
            """
            with self._universe_lock:
                initial_size = len(self._universe)
                now = datetime.datetime.now(tz=pytz.UTC)
                for element in elements:
                    self._universe[element][identifier] = now
                return initial_size != len(self._universe)

        def remove(self, identifier, elements):
            """
            Removes the monitoring of identifier from specific elements in the universe.
            Note that this method does *not* remove elements from the universe. The removal of
            elements is only done in the administrate method.

            Args:
                elements: The elements to remove active monitoring from
                identifier: The identifier monitoring the elements

            Returns: True if the universe is mutated, ie if new elements have been added
            """
            with self._universe_lock:
                for element in elements:
                    identifiers = self._universe.get(element, {})
                    if len(identifiers) and identifier in identifiers:
                        del identifiers[identifier]

        def clear(self):
            """
            Removes all active monitoring from the universe.

            Returns: True if the universe is mutated, ie if new elements have been added
            """
            with self._universe_lock:
                initial_size = len(self._universe)
                self._universe = defaultdict(dict)
                return initial_size > 0

    class IdleNodePool(object):
        def __init__(self, domain):
            self._logger = domain.logger_service.get_logger(self.__class__.__name__)
            self._idle_nodes_lock = RLock()
            self._idle_nodes = []

        def push(self, node_id, node_fut):
            with self._idle_nodes_lock:
                self._logger.info('{} -> available'.format(node_id))
                self._idle_nodes.append((node_id, node_fut))

        def pop(self):
            with self._idle_nodes_lock:
                if self._idle_nodes:
                    return self._idle_nodes.pop(0)
            return None, None

        def on_reallocation(self, allocations):
            with self._idle_nodes_lock:
                idle_nodes = []
                for (node_id, node_fut) in self._idle_nodes:
                    allocation = allocations.get(node_id)
                    if allocation is None or not allocation.universe:
                        idle_nodes.append((node_id, node_fut))
                        continue
                    node_fut.set_result(allocation)
                self._idle_nodes = idle_nodes

        def on_node_timeout(self, timed_out_node_id):
            with self._idle_nodes_lock:
                idle_list = []
                for (node_id, node_fut) in self._idle_nodes:
                    if node_id == timed_out_node_id:
                        self._logger.info('{} -> timed out')
                    else:
                        idle_list.append((node_id, node_fut))
                self._idle_nodes = idle_list

        def on_shutdown(self):
            exc = Exception('Shutting down')
            with self._idle_nodes_lock:
                for (node_id, node_fut) in self._idle_nodes:
                    self._logger.info('Releasing {}...'.format(node_id))
                    node_fut.set_exception(exc)
                self._idle_nodes = []

    class RunsQueueMonitor(object):
        def __init__(self, domain, node_handler, allocation_maker):
            self._node_handler = node_handler
            self._allocation_maker = allocation_maker
            self._logger = domain.logger_service.get_logger(self.__class__.__name__)
            self._pending_runs_lock = RLock()
            self._pending_runs = []
            self._pending_clients_lock = RLock()
            self._pending_clients = {}

        def on_run_allocated(self, node_id, element, client_id, client_fut=None):
            with self._pending_clients_lock:
                self._pending_clients[node_id] = (element, client_id, client_fut)
            self._logger.info('On-demand run {} from {} -> {}'.format(element, client_id, node_id))

        def on_run_completed(self, node_id):
            with self._pending_clients_lock:
                element, client_id, client_fut = self._pending_clients.pop(node_id,
                                                                          (None, None, None))
            if client_id:
                self._logger.info(
                    'Completed {} run on {} -> {}'.format(element, node_id, client_id))
                if client_fut:
                    client_fut.set_result(None)

        def on_node_available(self, node_id, node_fut):
            self.on_run_completed(node_id)
            element, client_id, client_fut = None, None, None
            with self._pending_runs_lock:
                if self._pending_runs:
                    element, client_id, client_fut = self._pending_runs.pop(0)
            if element:
                self.on_run_allocated(node_id, element, client_id, client_fut)
                node_fut.set_result(self._allocation_maker(element))
                return True
            return False

        def on_node_timeout(self, timed_out_node_id):
            with self._pending_clients_lock:
                element, client_id, client_fut = self._pending_clients.pop(timed_out_node_id,
                                                                          (None, None, None))
            if client_id:
                self._logger.info(
                    'Timed out {} run on {} -> {}'.format(element, timed_out_node_id, client_id))
                if client_fut:
                    client_fut.set_exception(Ice.ConnectionLostException())

        def on_shutdown(self):
            exc = Exception('Shutting down')
            with self._pending_clients_lock:
                for (element, client_id, client_fut) in self._pending_clients.values():
                    self._logger.info('Releasing {}...'.format(client_id))
                    client_fut.set_exception(exc)
                self._pending_clients = {}

        def queue(self, element, client_id, client_fut=None):
            node_id, node_fut = self._node_handler.pop()
            if node_id:
                self.on_run_allocated(node_id, element, client_id, client_fut)
                node_fut.set_result(self._allocation_maker(element))
            else:
                with self._pending_runs_lock:
                    self._logger.info(
                        'On-demand run {} from {} -> queued'.format(element, client_id))
                    self._pending_runs.append((element, client_id, client_fut))

    # endregion

    def __init__(self, domain):
        IceOnDemandAllocator.__init__(self)
        AllocatorServant.__init__(self, domain)
        self._timeout = self.domain.get_param('app', 'element_timeout',
                                              as_type=lambda t: datetime.timedelta(minutes=t),
                                              default=datetime.timedelta(minutes=15))
        self._universe_monitor = OnDemandAllocatorServant.UniverseMonitor(domain)
        self._idle_pool = OnDemandAllocatorServant.IdleNodePool(domain)
        self._run_queue = OnDemandAllocatorServant.RunsQueueMonitor(domain, self._idle_pool,
                                                                    self._make_run_allocation)
        self._shutting_down = False

    def ice_shutdown(self):
        self._shutting_down = True
        self._run_queue.on_shutdown()
        self._idle_pool.on_shutdown()
        self._universe_monitor.clear()
        super(OnDemandAllocatorServant, self).ice_shutdown()

    def _one_node_timeout(self, identifier):
        super(OnDemandAllocatorServant, self)._one_node_timeout(identifier)
        self._run_queue.on_node_timeout(identifier)
        self._idle_pool.on_node_timeout(identifier)

    def _allocate(self):
        """
        Calls _administrate_universe then the base class' _allocate method.
        We then check for idle nodes. If any, we immediately start them with their allocation.
        """
        self._universe_monitor.administrate(self._timeout)
        # reset _node_tasks and _node_load before allocate
        self._node_tasks = defaultdict(set)
        self._node_load = defaultdict(float)
        super(OnDemandAllocatorServant, self)._allocate()
        self._idle_pool.on_reallocation(self._allocations)

    def _assert_elements(self, elements):
        for element in elements:
            self._assert_element(element)

    def _assert_element(self, element):
        if not isinstance(element, self.UNIVERSE_ELEMENT_TYPES):
            raise ValidateException(
                invalid_object=element
                , reason='Invalid type {}, expecting {}'.format(type(element),
                                                                self.UNIVERSE_ELEMENT_TYPES)
            )

    def _make_run_allocation(self, element):
        raise NotImplementedError('{}._make_run_allocation'.format(self.__class__.__name__))

    def _is_allocation_valid(self, allocation):
        return allocation is not None and allocation.universe

    def add_to_universe(self, identifier, elements):
        """
        Adds elements to the universe allocated to the nodes. The OnDemandAllocator keeps track
        of the identifiers subscribed to an element, as well as how long they have been monitoring
        said elements.
        This method serves both to add elements to the universe as well as a heartbeat for the client
        itself.
        """
        if self._universe_monitor.add(identifier, elements):
            self._allocate()

    def remove_from_universe(self, identifier, elements):
        """
        Removes a client from specific elements in the universe allocated. Note that this
        method does *not* remove elements from the universe. The removal of elements is
        only done in the _administrate_universe method.
        """
        self._universe_monitor.remove(identifier, elements)

    def clear_universe(self):
        self._universe_monitor.clear()

    def run_elements(self, client_id, elements):
        for element in elements:
            self.run_element(element, client_id)

    def run_element(self, element, client_id, client_fut=None):
        """
        Allocate an element to a node for a single cycle. If a node is idle, we allocate the element
        to it immediately and keep track of the client callback. If no node is available, the element
        is added to a queue to be picked up as soon as a node is available.
        """
        self._run_queue.queue(element, client_id, client_fut)

    def getAllocation(self, identifier, current=None):
        """
        The getAllocation method is the crux of the OnDemandAllocator.
        We first check if the available node just completed a on-time cycle for a client. If it did
        we immediately release the client thread to signal the availability of the results.
        The next thing we check (other than whether the allocator is shutting down) is whether there
        are pending one-time runs. If they are, we immediately assign them to the available node.
        If we do have an allocation for this node, we run it.
        Otherwise we keep the node callback in an idle queue to have the node available for queries.
        """
        future = Ice.Future()
        # Shutting down, short-circuit the rest of the logic
        if self._shutting_down:
            future.set_exception(Exception('{} shutting down'.format(self.app_name)))
            return future

        # Pending on-demand runs *always* take precedence
        node_taken = self._run_queue.on_node_available(identifier, future)
        if node_taken:
            return future

        allocation = self._allocations.get(identifier)
        if self._is_allocation_valid(allocation):
            # If we have an allocation for the node, return it
            future.set_result(allocation)
        else:
            # Otherwise give the node the pool of idle nodes
            self._idle_pool.push(identifier, future)
        return future

    def add(self, identifier, elements, current=None):
        cxt = AMDContext('add|{}|{}'.format(identifier, elements), error_only=True)
        with cxt:
            self._assert_elements(elements)
            self.add_to_universe(identifier, elements)
        return cxt.future

    def remove(self, identifier, elements, current=None):
        cxt = AMDContext('remove|{}|{}'.format(identifier, elements), error_only=True)
        with cxt:
            self._assert_elements(elements)
            self.remove_from_universe(identifier, elements)
        return cxt.future

    def clear(self, current=None):
        cxt = AMDContext('clear', error_only=True)
        with cxt:
            self.clear_universe()
        return cxt.future

    def runElement(self, identifier, element, current=None):
        future = Ice.Future()
        try:
            self._assert_elements([element])
            self.run_element(element, identifier, future)
        except ValidateException as ve:
            future.set_exception(ve)
        except Exception as e:
            future.set_exception(e)
        finally:
            return future

    def getUniverse(self, current=None):
        cxt = AMDContext('getUniverse', error_only=True)
        with cxt:
            cxt.ice_return = self._universe_monitor.universe
        return cxt.future


class NodeServant(IceServant):
    DEFAULT_ALLOCATOR_PRX_NAME = None
    DEFAULT_ALLOCATOR_PRX_TYPE = AllocatorPrx
    DEFAULT_MUX_PROXY_TYPE = None
    NOTIFIER_SERVICE = None
    NO_ALLOCATION_TIMEOUT = 60

    def __init__(self, domain):
        super(NodeServant, self).__init__(domain)
        self._ice_service = self.domain.get_service(IceService)
        threadpool_service = self.domain.get_service(ThreadpoolService)
        self._subscription_pool = threadpool_service.get_pool(self.__class__.__name__)

        self._allocation = self.domain.get_param('app', 'allocation', default=None)
        self._use_allocator = self.domain.get_param('app', 'use_allocator', default=True)

        if self._use_allocator:
            alloc_prx_name = self.domain.get_param('app', 'allocator_proxy_name',
                                                   default=self.DEFAULT_ALLOCATOR_PRX_NAME)
            assert alloc_prx_name, 'allocator_proxy_name cannot be None, override in derived class'
            self._allocator = self._ice_service.get_proxy(alloc_prx_name,
                                                          self.DEFAULT_ALLOCATOR_PRX_TYPE)
            if self._allocator is None:
                raise RuntimeError('Could not get allocator proxy {}'.format(alloc_prx_name))
        self._mux_proxy_names = self.domain.get_param('app', 'mux_proxy_names', default=[])
        self._mux_proxy_type = self.domain.get_param('app', 'mux_proxy_type', default=self.DEFAULT_MUX_PROXY_TYPE)
        self._identity = Identity(self.app_name, datetime.datetime.now().isoformat())
        self._adp_cache = set()

        assert self.NOTIFIER_SERVICE, 'NOTIFIER_SERVICE cannot be None, override in derived class'
        self.proxy_cache = domain.get_service(ListenerProxyCache)
        self.notifier = domain.get_service(self.NOTIFIER_SERVICE)

        self._timer_event = Event()

        cycle_interval = self.domain.get_param('app', 'cycle_interval', default=120)
        self._cycle_timer = Timer(self._timer_event, self._execute_cycle, cycle_interval,
                                  name='CycleThread')

        self._cycle_id = 0
        self._cycles_failed = 0
        self._cycle_failure_limit = self.domain.get_param('app', 'cycle_failure_limit', default=25)

        heartbeat_interval = self.domain.get_param('app', 'heartbeat_interval', default=5)
        self._heartbeat_timer = Timer(self._timer_event, self._heartbeat, heartbeat_interval,
                                      name='HeartBeatThread')

    def ice_init(self):
        self.logger.info('Starting {}'.format(self.app_name))
        self._heartbeat_timer.start()
        self._register()
        self._cycle_timer.start()
        self.logger.info('{} ready'.format(self.app_name))

    def ice_shutdown(self):
        self._timer_event.set()
        self.logger.info('{} shutting down'.format(self.app_name))
        if self._cycles_failed > self._cycle_failure_limit:
            exit(99)

    def terminate(self):
        self._ice_service.communicator.shutdown()

    @property
    def ice_servant(self):
        return None

    @property
    def self_heartbeat(self):
        return False

    def _heartbeat(self):
        if self._use_allocator:
            self._allocator.register(self.app_name)

    def _add_adapter(self, proxy):
        key = (self, self._identity, proxy)
        if key not in self._adp_cache:
            proxy.ice_getConnection().getAdapter().add(self, self._identity)
            self._adp_cache.add(key)

    def _mux_keys(self):
        raise NotImplementedError('_mux_keys must be implemented')

    def _register(self):
        for proxy_name in self._mux_proxy_names:
            with TimeIt(logger=self.logger, tag='Grabbing {}'.format(proxy_name)):
                proxy = self._ice_service.get_proxy(proxy_name, self._mux_proxy_type)
                if proxy is None:
                    raise RuntimeError('Failed to get proxy \'{}\' (type {})'.format(proxy_name, self._mux_proxy_type))
                self._add_adapter(proxy)
            # TODO Right now we subscribe with a single mux key so the server does a universal subscription back
            for mux_key in self._mux_keys():
                tag = 'Register {} with proxy {} @ identity {}'.format(mux_key, proxy_name,
                                                                       self._identity)
                with TimeIt(logger=self.logger, tag=tag):
                    proxy.registerDestination(self._identity, mux_key)

    def _execute_allocation(self, allocation):
        raise NotImplementedError('{}._execute_allocation'.format(self.__class__.__name__))

    def _assert_allocation(self, allocation):
        raise NotImplementedError('{}._assert_allocation'.format(self.__class__.__name__))

    def _execute_cycle(self):
        self._cycle_id += 1
        # arbitrary cycle cut-off after N consecutive failures
        if self._cycles_failed > self._cycle_failure_limit:
            self.logger.error(
                'Too many cycle failures ({}), terminating node.'.format(self._cycles_failed))
            self.terminate()
        with TimeIt(logger=self.logger, tag='Cycle #{:0>6d}'.format(self._cycle_id)):
            allocation = self._allocation
            if self._use_allocator:
                with TimeIt(logger=self.logger,
                            tag='Cycle #{:0>6d} Get Allocation'.format(self._cycle_id)):
                    try:
                        self.logger.info('Requesting allocation from {}'.format(self._allocator))
                        allocation = self._allocator.getAllocation(self.app_name)
                    except:
                        self.logger.exception(
                            'Failed getting allocation, aborting cycle #{:0>6d}'.format(
                                self._cycle_id))
                        self._cycles_failed += 1
                        return
            try:
                self._assert_allocation(allocation)

                with TimeIt(logger=self.logger,
                            tag='Cycle #{:0>6d} Execute Allocation'.format(self._cycle_id)):
                    try:
                        self._execute_allocation(allocation)
                    except Exception as e:
                        self.logger.exception('Failed cycle #{:0>6d}:\n{}'.format(self._cycle_id, e))
                        self._cycles_failed += 1
                    else:
                        self._cycles_failed = 0

            except NoAllocationException as e:
                self.logger.warn('No allocations in cycle #{:0>6d}'.format(self._cycle_id))
                time.sleep(self.NO_ALLOCATION_TIMEOUT)

    def _alter_subscription(self, notifier_func, current, ident, sub_arg):
        try:
            self.logger.info('Acquiring {}...'.format(ident))
            px = self.proxy_cache.get_proxy(ident, self.notifier.proxy_type, current)
            self.logger.info('Acquired {}'.format(ident))
            self.logger.info('Calling {} on {} with {}...'.format(notifier_func, ident, sub_arg))
            notifier_func(self.notifier, ident, px, sub_arg)
            self.logger.info('Called {} on {} with {}'.format(notifier_func, ident, sub_arg))
        except:
            self.logger.exception('Failed to call {} on {} with {}'.format(notifier_func, ident, sub_arg))

    def _remove_subscription(self, ident, sub_arg):
        try:
            if self.notifier.unsubscribe(ident, sub_arg):
                self.proxy_cache.remove_proxy(ident, self.notifier.proxy_type)
        except:
            self.logger.exception('Failed to unsubscribe {} with {}'.format(ident, sub_arg))

    def _subscribe(self, method_name, current, ident, sub_id):
        cxt = AMDContext(method_name, True)
        with cxt:
            self._subscription_pool.add_task(
                self._alter_subscription
                , self.NOTIFIER_SERVICE.subscribe
                , current
                , ident
                , sub_id
            )
        return cxt.future

    def _subscribe_all(self, method_name, current, ident, sub_ids):
        cxt = AMDContext(method_name, True)
        with cxt:
            self._subscription_pool.add_task(
                self._alter_subscription
                , self.NOTIFIER_SERVICE.subscribe_all
                , current
                , ident
                , sub_ids
            )
        return cxt.future

    def _update_subscriptions(self, method_name, current, ident, sub_ids):
        cxt = AMDContext(method_name, True)
        with cxt:
            self._subscription_pool.add_task(
                self._alter_subscription
                , self.NOTIFIER_SERVICE.update_subscriptions
                , current
                , ident
                , sub_ids
            )
        return cxt.future

    def _unsubscribe(self, method_name, ident, sub_id):
        cxt = AMDContext(method_name, True)
        with cxt:
            self._subscription_pool.add_task(
                self._remove_subscription
                , ident
                , sub_id
            )
        return cxt.future

