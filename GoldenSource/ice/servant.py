import time

import Ice

from GoldenSource.common.domain import Domain
from GoldenSource.common.runner import Application
from GoldenSource.error.parse import BadConfigException
from GoldenSource.ice.ice_service import IceService

class IceServant(Application):
    """
    An IceServant is an application that eventually registers to the IceRegistry and provides some capability to the system.
    """

    def __init__(self, domain) -> None:
        super().__init__(domain)
        self.ice_service = domain.get_service(IceService)

    @property
    def ice_servant(self):
        """
        This property must return the iceServant that will be registered. 
        """
        return self
    
    def run(self):
        """
        Run the IceServant.
        """
        with self.ice_servant.context(self.ice_shutdown, servant_handler=self.ice_servant, self_heartbeat=self.self_heartbeat):
            self.ice_init()

    def ice_init(self):
        """
        This method is called after the Ice communicator is created and configured, and before the servant gets activated.
        """
        raise BadConfigException("app.run_class must be specified in the configuration in order to use the Runner")
    
    @staticmethod
    def get_client_ip(current):
        """
        :param current: "Current" object from the ice client connection
        :return IPAddress and the Port number of the client connection
        Fetches the client ip address based on the client connection
        """
        if current is not None:
            if current.con is not None:
                c_info = current.con.getInfo()
                if c_info is not None:
                    return c_info.remoteAddress + ":" + str(c_info.remotePort)
                else:
                    return "[Empty current connection Info]"
            else:
                return "[Empty current connection]"
        else:
            return "[Empty current]"
    
    def ice_shutdown(self):
        """
        This method is called when the IceServant is shutting down.
        """
        pass

    @property
    def self_heartbeat(self):
        """
        This property must return the heartbeat monitoring service.
        """
        return True
    

class AMDContext(object):
    """
    Convenient wrapper for [AMD]-type ice calls. The AMDContext will take care of handling the exceptions properly 
    and setting up the future to send back the data to the client.
    All the arguments passed are optional, they really serve for logging purposes.

    You must remember to capture the future object or create the AMDContext outside of the scope of the "with" block. 
    No Matter what, the future must be returned by the AMD method in Ice. If you capture, it should be the very first 
    line of your 'with' block to mitigate against the possibility of an exception being raised before you capture the future object.

    Note that raising an exception from inside the 'with' block does not exit the containing function, however returning does. 
    If you return from within the 'with' block, the containing function will return and control will be passed back to the caller.
    You must return the future object.

    If an exception is raised inside the 'with' block, the future will be set accordingly, however control flow after the with block will continue.

    As a result, the future must always be returned after the with block because this is the only way to guarantee that the future is returned by the 
    function in case an exception occurs in the 'with' block.

    Usage Example 1:
    class IceServant(...):
        def myCallbackFunction(..., current=None):
            future = None
            with AMDContext("IceServant", "myCallbackFunction") as cxt:
                # Always capture the future before doing anything else
                future = cxt.future
                <logic goes here>
                cxt.ice_return = <return_value>
                # Returning the future from within the 'with'block is fine.
                # But you still have to return the future after the 'with' block
                return cxt.future
            # Return here in case exception is raised in 'with' block
            return cxt.future

    
    Usage Example 2:
    class IceServant(...):
        def myCallbackFunction(..., current=None):
            cxt = AMDContext("IceServant", "myCallbackFunction")
            with cxt:
                <logic goes here>
                cxt.ice_return = <return_value>
            return cxt.future

    Usage Example 3:
    class IceServant(...):
        def myCallbackFunction(..., current=None):
            cxt = AMDContext("IceServant", "myCallbackFunction")
            with cxt:
                <logic goes here>
                raise ValueError("Something broke)
            # Make sure future gets returned if raise occurs
            return cxt.future

    """

    def __init__(self, prefix="", error_only=False) -> None:
        self.logger = Domain().logger_service.get_logger(self.__class__.__name__)
        self.future = Ice.Future()
        self.prefix = prefix
        self.error_only = error_only
        self.ice_return = None

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.future.set_exception(exc_val)
            self.logger.error("{prefix}|{exception}".format(prefix=self.prefix, exception=self.logger.ex2str(exc_type, exc_val, exc_tb)))

        else:
            self.future.set_default(self.ice_return)

            if not self.error_only:
                self.logger.info("{prefix}|Completed".format(prefix=self.prefix))
        return True
    

class AMDTimerContext(AMDContext):
    """
    An AMDContext that keep timers running to track performance of the ice calls
    """

    def __init__(self, prefix="", error_only=False) -> None:
        super().__init__(prefix, error_only)

        self.future = Ice.Future()
        self.logic_timer = None
        self.marshalling_timer = None

    def __enter__(self):
        self.logic_timer = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logic_timer = time.time() - self.logic_timer
        if exc_type is not None:
            self.marshalling_timer = time.time()
            self.future.set_exception(exc_val)
            self.marshalling_timer = time.time() - self.marshalling_timer

            self.logger.exception("{prefix}|[logic:{ltimer:.6f},marshalling:{mtimer:.6f}]|{exception}".format(
                prefix=self.prefix, 
                ltimer=self.logic_timer,
                mtimer=self.marshalling_timer,
                exception=self.logger.ex2str(exc_type, exc_val, exc_tb)))
        else:
            self.marshalling_timer
            if self.ice_return is not None:
                self.future.set_result(self.ice_return)
            else:
                self.future.set_default(None)
            self.marshalling_timer = time.time() - self.marshalling_timer

            if not self.error_only:
                self.logger.info("{prefix}|[logic:{ltimer:.6f},marshalling:{mtimer:.6f}]|Completed".format(
                    prefix=self.prefix,
                    ltimer=self.logic_timer,
                    mtimer=self.marshalling_timer))
        return True
