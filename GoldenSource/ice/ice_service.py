from threading import Lock
import Ice
import contextlib
import functools
import threading
import traceback
import os
from collections import defaultdict

from GoldenSource.common.concurrency import Trigger
from GoldenSource.utils.patterns import Singleton
from GoldenSource.common.services import Service

class ProxyHandler(object):

    def __init__(self) -> None:
        self.proxy = None
        self.lock = Lock()

class ProxyReconnecter(object):
    pass

class ProxyTrigger(Trigger):
    def __init__(self, proxy_name, proxy_method, *method_args, **method_kwargs) -> None:
        super(ProxyTrigger, self).__init__()
        self._proxy_name = proxy_name
        self._proxy_method = proxy_method
        self._method_args = method_args
        self._method_kwargs = method_kwargs

    def trigger(self, domain):
        ice_service = domain.get_service(IceService)
        proxy = ice_service.get_proxy(self._proxy_name, self._proxy_method.im_class)
        self._proxy_method(proxy, *self._method_args, **self._method_kwargs)

###############
### ICE SERVICE
###############

class IceService(Service):
    """
    Entry point to the ice platform. This sets up the ice layer and provides methods to grab proxies seamlessly.
    It alternatively allows to activate a servant and will make the main thread wait until the servant is shutdown.
    Another useful usecase involves simply calling the wait_for_shutdown()/destroy() methods for ice clients.
    Lastly, access to the underlying communicator object is granted through the read-only communicator property.
    """

    def __init__(self, domain) -> None:
        super(IceService, self).__init__(domain)
        self.logger = domain.get_service(domain.logger_type).get_logger(IceService.__name__)
        self._environment = domain.get_param("environment")
        self._app_name = domain.get_param("app", "full_name")
        self._ice_config = domain.get_param("Ice", default={})
        self._wait_for_proxy_in_main_thread = domain.get_param("app" ,"wait_for_proxy_in_main_thread", default = False)
        self._domain = domain
        self._proxy_props = {}
        self.load_proxy_definitions(domain.get_param("proxies"))

        self.proxy_cache = {}
        self.proxy_lock = Lock()
        self._communicator = None
        self.shutdown_called = False
        self.initialize_ice()

    @property
    def communicator(self):
        return self._communicator
    
    @property
    def proxy_definitions(self):
        return {proxy_id[0]: proxy_def for proxy_id, proxy_def in self._proxy_props.items()}
    

    def load_proxy_definitions(self, proxy_props):
        if not proxy_props:
            self.logger.warn("No proxies defined")
            return
        
        for proxy_id, proxy_info in proxy_props.items():
            proxy_string = proxy_info.get("ps", "{0} @ {0}".format(proxy_id))
            proxy_type = proxy_info.get("class")
            tidal = proxy_info.get("tidal", "{}_READY_{}".format(proxy_id.upper().replace(".", "_").replace("/", "_").replace("\\", "_"), self._environment.upper()))
            endpoint = proxy_info.get("endpoint")
            if proxy_type is None:
                self.logger.warn("Skipping {id} proxy, no proxy type defined. Please set {id}.'class' the relevant value.".format(id=proxy_id))
                continue
            self._proxy_props[(proxy_id, proxy_type)] = {
                "ps": proxy_string,
                "class": proxy_type,
                "tidal": tidal,
                "endpoint": endpoint
            }

    def initialize_ice(self, config=None, override=False):
        """
        Initializes the ice communication layer. Config is, by default, read at construction time from the configuration service.
        The initialization can be reset at any time later on via providing an alternate configuration.
        The proxies already opened will be cleared and will have to be reinitiated.

        Arguments:
            - config: A dictionary defining the various ice properties
            - override: True if config should only override the specified Ice environment values.
        """
        if config is None:
            config = self._ice_config
        elif override:
            for k, v in self._ice_config.items():
                if k not in config:
                    config[k] = v
        
        props = Ice.createProperties()
        for key, value in config.items():
            props.setProperty(key, value)
        props.setProperty('Ice.ImplicitContext', 'Shared')

        init_data = Ice.InitializationData()
        init_data.properties = props
        self._communicator = Ice.initialize(init_data)
        self.proxy_cache = {}
        ctx = self._communicator.getImplicitContext()
        if ctx is not None:
            caller_info = "{app_name}@{machine_name}"
            caller_info = caller_info.format(
                app_name = self._domain.get_param("app", "full_name", default="Unknown App"),
                machine_name = os.environ.get("COMPUTERNAME", "Unknown Machine")
            )
            ctx.put("Remote", caller_info)
        
    def get_proxy_info(self, proxy_id, field=None):
        """
        Returns the proxy information the given pxid. pxid can be a name {"instruments", or "refdata"} or 
        a proxy type (e.g. GoldenSource.interfaces.InstrumentsPrx or GoldenSource.interfaces.RefDataPrx)
        If a type is specified, the list found occurence of such a proxy will be returned.

        Arguments:
            - pxid The name or type of the proxy
        
        Returns:
        The Proxy information, a dictionary of key-based configuration information
        """
        for proxy_tuple, proxy_info in self._proxy_props.items():
            if proxy_id in proxy_tuple:
                if field:
                    return proxy_info[field]
                else:
                    return proxy_info
    
    def get_proxy(self, proxy_id, proxy_type=None, no_wait=False):
        """
        Returns the proxy with the given pxid. pxid can be a name {"instruments", or "refdata"} or 
        a proxy type. 
        If a type is specified, the first occurence of such a proxy will be returned.
        Arguments:
            - pxid The name or type of the proxy
            - proxy_type The type of the proxy if pid is the full name
            - no_wait If True, the method will not wait for the proxy to be ready.
        """
        if self.shutdown_called:
            raise RuntimeError("Ice communicator has been shutdown")
        
        request_prx_id = proxy_id
        request_proxy_type = None

        # Check if i have already configured the class and other configs for this proxy
        for proxy_tuple, proxy_info in self._proxy_props.items():
            _id, _type = proxy_tuple
            if proxy_id == _id:
                request_prx_id = _id
                request_proxy_type = _type
                break
        
        if request_proxy_type is None and proxy_type is not None:
            self._generate_proxy_info(proxy_id, proxy_type)
            request_proxy_type = proxy_type

        handler = None
        with self.proxy_lock:
            # Cache a blank handler to maintain singleton status of this proxy
            for k, v in self.proxy_cache.items():
                if proxy_id in k:
                    handler = v
            
            if handler is None:
                # Create new handler since this is first time
                handler = ProxyHandler()
                self.proxy_cache[(request_prx_id, request_proxy_type)] = handler

        # This lock is proxy specific, it wont block if some other thread tries to create a different proxy
        with handler.lock:
            # Everything regarding this handler is not synchronized
            if handler.proxy is not None:
                try:
                    # Is the proxy currently up? maybe it got disconnected
                    handler.proxy.ice_ping()
                    return handler.proxy
                except:
                    handler.proxy = None

            # Proxy is not connected, create a new proxy
            prev_error = None
            try:
                handler.proxy = self._new_proxy(request_prx_id, request_proxy_type)
            except Exception as e:
                self.logger.error("Failed to connect first attempt {}, Exception: {}".format(request_prx_id, str(e)))
                prev_error = e
                handler.proxy = None

            # Am i allowed to wait in main thread until the proxy is connected?
            # Is the proxy already connected?
            # Is this a main thread?
            
            if handler.proxy is None and self._wait_for_proxy_in_main_thread \
                and hasattr(self._domain, "main_thread") \
                and threading.current_thread() == self._domain.main_thread \
                and not no_wait:
                
                alerted = False
                while handler.proxy is None and not self.shutdown_called:
                    try:
                        # Not printing too many logs in reconnection loop
                        handler.proxy = self._new_proxy(request_prx_id, request_proxy_type, False)
                    except Exception as e:
                        # Error in retry loop, no need to print
                        handler.proxy = None
                    
                    if handler.proxy is None:
                        if not alerted:
                            from GoldenSource.infra.alert import AlertService

                            self._domain.get_service(AlertService).raise_alert("IceService", "IceService",
                                                                               AlertService.Critical,
                                                                               "Waiting for dependent server: " + request_prx_id)
                            alerted = True
                        self.logger.info("Waiting for proxy to be connected: {}...".format(request_prx_id))
                        e = threading.Event()
                        e.wait(timeout=3)
                if alerted:
                    from GoldenSource.infra.alert import AlertService
                    self._domain.get_service(AlertService).raise_alert("IceService", "IceService",
                                                                            AlertService.Information,
                                                                            "Connected dependent server: " + request_prx_id)
                
            elif prev_error is not None:
                raise prev_error
            
            return handler.proxy
        
    def activate_servant(self, handler, proxy_id=None):
        """
        Activate the srevant defined by pxid. If no pxid is specifed, the proxy specified on the command line will be used.
        
        Arguments:
            - handler The object to handle the servant's callback
            - pxid The name of the proxy to activate
        """

        assert handler is not None, "Cannot activate servant with None handler"

        proxy_info = self.get_proxy_info(proxy_id)
        if proxy_info is None:
            proxy_info = self._generate_proxy_info(proxy_id, type(handler), do_cache=False)

        servant_id = proxy_info["ps"]
        assert servant_id is not None, "Cannot activate servant [{}], no 'ps' setup".format(proxy_id)
        servant_split = servant_id.split("@")
        assert len(servant_split)==2, "Cannot activate servant [{}], 'ps' setup is invalid with value [{}]".format(proxy_id, servant_id)

        servant_name, adapter_name = (s.strip() for s in servant_split)

        ice_props = self._communicator.getProperties()
        ice_props.setProperty("{}.AdapterId".format(servant_name), adapter_name)
        ice_props.setProperty("{}.Endpoints".format(servant_name), "tcp")

        servant_identity = self._communicator.stringToIdentity(servant_name)
        endpoint = proxy_info.get("endpoint")
        if endpoint is not None:
            adapter = self._communicator.createObjectAdapterWithEndpoints(adapter_name, endpoint)
        else:
            adapter = self._communicator.createObjectAdapter(adapter_name)

        adapter.add(handler, servant_identity)
        adapter.activate()
        self.logger.info("Servant [{}] activated".format(servant_id))
        self.set_tidal_variable(proxy_info.get("tidal"), 1)

    def deactivate_servant(self, handler, proxy_id=None):
        proxy_info = self.get_proxy_info(proxy_id)
        if proxy_info is None:
            proxy_info = self._generate_proxy_info(proxy_id, None, do_cache=False)
        
        servant_id = proxy_info["ps"]
        self.logger.info("{} servant deactivated".format(servant_id))
        self.set_tidal_variable(proxy_info.get("tidal"), 0)

    def set_tidal_variable(self, tidal, value):
        if tidal is not None:
            try:
                tidal_proxy = self.get_proxy("tidalserver")
                tidal_proxy.setVariable(tidal, str(value))
            except:
                self.logger.exception("Failed to set tidal variable: {!s}={!s}".format(tidal, value))
            else:
                self.logger.info("Set tidal variable: {!s}={!s}".format(tidal, value))
        else:
            self.logger.info("No tidal variable to set")

    def wait_for_shutdown(self):
        """
        Waits for the communicator to be destroyed.
        """
        self._communicator.waitForShutdown()

    def shutdown(self):
        """
        Destroys the ice layer, effectively shuting down all inbound and outbound connections.
        """
        self.shutdown_called = True
        self.logger.info("Shutting down Ice Service")
        if self._communicator:
            # Clean up
            try:
                self._communicator.destroy()
                self._communicator = None
            except:
                self.logger.critical(self.logger.ex2str())
                traceback.print_exc()

    @contextlib.contextmanager
    def context(self, *callbacks, **kwargs):
        """
        Ice context activation. Allows the following syntactic suger:
        with ice_service.context():
            # Do something
        
        @type calbacks: list of callables
        @param callbacks: A list of callables to be called upon context activation

        @type kwargs: dictionary
        @param kwargs: A dictionary of keyword arguments to be passed to the callbacks

        @type servant_handler: servant
        @param servant_handler: If not None, the context will call activate_servant on the handler provided. Default is None

        @type proxy_id: string
        @param proxy_id: The proxy id to use when activating the servant handler. If not specified, the config full_name will be used

        @type wait_for_shutdown: boolean
        @param wait_for_shutdown: If True, the context will wait for shutdown after the block is executed. Default is True
        
        @type shutdown_on_exit: boolean
        @param shutdown_on_exit: If True, the context will call shutdown on the ice service upon exit. Default is True
        """
        servant_handler = kwargs.get("servant_handler")
        proxy_id = kwargs.get("proxy_id", self._app_name)
        wait_for_shutdown = kwargs.get("wait_for_shutdown", True)
        self_heartbeat = kwargs.get("self_heartbeat", True)
        shutdown_on_exit = kwargs.get("shutdown_on_exit", True)

        try:
            # Gives the handle back to the caller to execute the with block, returning the ice service for conveniency
            yield self

            if servant_handler:
                self.activate_servant(servant_handler, proxy_id)
            
            # Wait for shutdown
            if wait_for_shutdown:
                # Start heartbeat before waiting for shutdown, all ice servants will by default heartbeat
                # all those apps that are not Ice servants but rely on this call to keep them running will also HB
                # All Ice servants will activate heartbeat, it starts self heartbeat automatically
                if self_heartbeat and self._domain.configuration.name is not None:
                    self._domain.get_service(HeartBeatMonitoringService).add_process_to_heartbeat(self._domain.configuration.name)
                
                self.wait_for_shutdown()
        except KeyboardInterrupt:
            # Ignore CTRL+C signals
            pass
        finally:
            if servant_handler:
                self.deactivate_servant(servant_handler, proxy_id)
            
            for cb in callbacks:
                try:
                    cb()
                except:
                    self.logger.error("On ice service context exit, calling [{}]".format(cb.__name__ if hasattr(cb, "__name__") else cb))

            if shutdown_on_exit:
                self.shutdown()
    
    def _new_proxy(self, proxy_id, proxy_type, debug=True):
        """
        Creates a new proxy for the given proxy_id and proxy_type. The proxy is returned if successful, otherwise None is returned.
        """
        proxy_info = self._proxy_props[(proxy_id, proxy_type)]
        proxy_endpoint = proxy_info.get('endpoint')
        if proxy_endpoint and '-h' in proxy_endpoint and '-p' in proxy_endpoint:
            proxy_string = '{} : {}'.format(proxy_id, proxy_endpoint)
        else:
            proxy_string = proxy_info['ps']
        proxy_class = proxy_info['class']

        if debug:
            self.logger.info("Grabbing {}...".format(proxy_string))
        base_proxy = self._communicator.stringToProxy(proxy_string)
        proxy = proxy_class.checkedCast(base_proxy)
        assert proxy, "Checked cast of base proxy into {} failed".format(proxy_class.__name__)
        self.logger.info("Grabbed {}...".format(proxy_string))
        #Always add a default adapter
        proxy.ice_getConnection().setAdapter(self._communicator.createObjectAdapter(""))

        return proxy
    
    def _generate_proxy_info(self, proxy_id, proxy_type, do_cache=True):
        """
        Generates a proxy info for the given proxy_id and proxy_type. The generated proxy info is returned.
        """
        proxy_info = {}
        if "@" in proxy_id:
            proxy_info["ps"] = proxy_id
        else:
            proxy_info["ps"] = "{0} @ {0}".format(proxy_id)
        proxy_info["class"] = proxy_type
        if do_cache:
            self._proxy_props[(proxy_id, proxy_type)] = proxy_info
        return proxy_info


