import datetime
import math
import os

from collections import defaultdict
from threading import Event, RLock

import Ice
from Ice import Identity
from GS.dataobjects import OnDemandAllocation
from GS.exceptions import ValidateException
from GS.interfaces import Allocator as IceAllocator, AllocatorPrx, OnDemandAllocator as IceOnDemandAllocator

from GoldenSource.common.concurrency import Timer, ThreadpoolService
from GoldenSource.ice.ice_service import IceService, ListenerProxyCache
from GoldenSource.ice.servant import AMDContext, IceServant
from GoldenSource.utils.patterns import TimeIt
# from GoldenSource.monitoring.heartbeat_service import HeartBeatMonitoringService
import time

class NoAllocationException(Exception):
    def __init__(self, message):
        super(NoAllocationException, self).__init__(message)

class NodeTask(object):
    """
    Generic task for a node. Computes its own cost of execution.

    TOTAL_COST = DEFAULT_COST * DEFAULT_FACTOR + DEFAULT_WEIGHT

    Can be weighted by the identifer of the task:
    TOTAL_COST = COST_MAP[self.identifier] * FACTOR_MAP{self.identifier} + WEIGHT_MAP[self.identifier]

    Can include cost floor by using MIN_COST:
    TOTAL_COST = TOTAL_COST if TOTAL_COST > 0 else MIN_COST
    """

    DEFAULT_COST = 1
    DEFAULT_FACTOR = 1
    DEFAULT_WEIGHT = 0
    MIN_COST = 0.1

    def __init__(self, domain, identifier) -> None:
        super().__init__()
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
        cost = self.DEFAULT_COST * self.DEFAULT_FACTOR + self.DEFAULT_WEIGHT
        self._cost = cost if cost > 0 else self.MIN_COST

    def __hash__(self) -> int:
        return hash(self.identifier)
    
    def __cmp__(self, other):
        if self.identifier > other.identifier:
            return 1
        elif self.identifier < other.identifier:
            return -1
        return 0
    
    def __str__(self) -> str:
        return '{}(id=<{}>, work={:>4.2f})'.format(
            self.__class__.__name__,
            self.identifier,
            self.cost
        )
    
    def __repr__(self) -> str:
        return self.__str__()
    

class AllocatorServant(IceAllocator, IceServant):
    DEFAULT_NODE_COUNT = 0
    DEFAULT_NODE_TIMEOUT = None
    DEFAULT_NODE_BASE_NAME = None
    DEFAULT_NODE_CONFIG = None
    DEFAULT_NODE_LOCATION = None
    DEFAULT_NODE_SCRIPT = None
    DEFAULT_ALLOCATION_CLASS = None

    def __init__(self, domain):
        IceAllocator.__init__(self)
        IceServant.__init__(self, domain)

        self._event = Event()
        self._node_watch = {}
        self._node_spawn_watch = {}

        self._no_spawn = domain.get_param('app', 'no_spawn', False)
        self._no_re_spawn = domain.get_param('app', 'no_re_spawn', True)
        self._node_count = self.domain.get_param('app', 'node_count', self.DEFAULT_NODE_COUNT)
        assert self._node_count > 0, "app.node_count parameter is mandatory"
        self._scale = int(math.log10(self._node_count)) + 1

        self._node_timeout = self.domain.get_param('app', 'node_timeout', self.DEFAULT_NODE_TIMEOUT)
        self._node_base_name = self.domain.get_param('app', 'node_base_name', self.DEFAULT_NODE_BASE_NAME)
        assert self._node_base_name, "app.node_base_name parameter is mandatory"
        default_node_config = self.DEFAULT_NODE_CONFIG
        if default_node_config is None:
            default_node_config = os.path.join(domain.configuration.config_path, '{}.cfg'.format(self._node_base_name))
        self._node_config = self.domain.get_param('app', 'node_config', default_node_config)
        assert self._node_config, "app.node_config parameter is mandatory"

        self._node_command_line = self.domain.get_param('app', 'node_command_line')

        self._node_location = self.domain.get_param('app', 'node_location', self.DEFAULT_NODE_LOCATION)
        if self._node_location is None:
            self.logger.warning("app.node_location parameter is not set, using default value")

        self._node_script = self.domain.get_param('app', 'node_script', self.DEFAULT_NODE_SCRIPT)

        self._allocation_clazz = self.domain.get_param('app', 'allocation_class', self.DEFAULT_ALLOCATION_CLASS)

        assert self._allocation_clazz, "app.allocation_class parameter is mandatory"

        self._allocations = {}
        self._node_taks = defaultdict(set)
        self._node_load = defaultdict(float)
        # self.heartbeat_service = self.domain.get_service(HeartBeatMonitoringService)
        self._all_nodes_ready = False
        if self._no_spawn:
            self.logger.info("Node Spawn is disabled. Nodes wont be started")
        else:
            self.logger.info("Node Spawn is enabled. Nodes will be started")

        self._tasks = {}

    
