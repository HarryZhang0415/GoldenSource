import atexit
from threading import Lock
import traceback
import sys

from GoldenSource.python.common.config import Configurator
from GoldenSource.python.common.services import LoggerService
from GoldenSource.python.utils.patterns import Singleton

class Domain(dict, metaclass=Singleton):
    """
    The domain holds the configuration of the currently running application
    Its second and foremost use is the instantiation and resgistation of services
    """
    # __metaclass__ = Singleton // Python 2.7

    def __init__(self, configurator_type=Configurator, logger_type=LoggerService):
        """
        Initializess the domain using the configurator and logger classes passed as argument.
        :param configurator_type: The configurator responsible for parsing the command line and loading the parameters
        :param logger_type: The logger service responsible for generating the various loggers throughout the application
        """
        super(Domain, self).__init__()
        self._service_lock = Lock()
        self._service_stack = []
        self.main_thread = None

        self._configurator_type = configurator_type
        self._configurator = configurator_type()
        self._configurator.parse()

        self._logger_type = logger_type 
        self._logger_service = logger_type(self)
        self.register_service(logger_type, self._logger_service)
        self.logger = self._logger_service.get_logger(Domain.__name__)

        self._verbose = self._configurator.get_param(self.__class__.__name__, 'verbose', as_type=bool, default=False)

        atexit.register(self.shutdown)
    
    @property
    def logger_type(self):
        return self._logger_type
    
    @property
    def logger_service(self):
        return self._logger_service
    
    @property
    def configuration(self):
        return self._configurator
    
    def _make_service(self, service_clazz, service_builder=None):
        """
        Initializes a service and resgister it in the domain.
        :param service_clazz: The class of the service to be instantiated
        :param service_builder: The factory to be used to instantiate the service
        :return: The service instance
        """
        # Resolve the service constructor
        maker = service_clazz
        if service_builder is not None:
            maker = service_builder
        
        if self._verbose and self.logger:
            self.logger.debug("Initializing {}".format(service_clazz.__name__))
        service = maker(self)

        # Register the service to the domain
        self.register_service(service_clazz, service)

        if self._verbose and self.logger:
            self.logger.debug("Initialization of {} complete".format(service_clazz.__name__))

        # Return the newly created & initialized service
        return service

    def register_service(self, service_clazz, service):
        """
        Registers a service to the domain
        :param service_clazz: The class of the service to be registered
        :param service: The service instance to be registered
        """
        # Service resgistration
        # Note that there is obsolutely no check whatsoever
        self[service_clazz] = service
        self._service_stack.append(service)
    
    def get_service(self, service_clazz, service_builder=None):
        """
        Retrieves a service instance for the class. Potentially instantiating and registering it if needed
        :param service_clazz: The class of the service to be retrieved
        :param service_builder: The factory to be used to instantiate the service
        :return: The service instance
        """
        # Returns the cached service if it exists, otherwise try to make it
        service = self.get(service_clazz)
        if service is None:
            with self._service_lock:
                service = self.get(service_clazz)
                if service is None:
                    service = self._make_service(service_clazz, service_builder)
        return service

    def __missing__(self, service_clazz):
        """
        When the domain's bracket operator is called against a service still not instantiated, effectively instantiate it and return
        :param service_clazz: The class of the missing service
        :return: The newly instantiated service
        """
        with self._service_lock:
                service = self.get(service_clazz)
                if service is None:
                    service = self._make_service(service_clazz)
        return service
    
    def get_param(self, *nodes, **kwargs):
        """
        Returns the configuration parameters. Shortcut to the configurator's get_param method
        """
        # Convenient call to the underlying configurator
        return self._configurator.get_param(*nodes, **kwargs)
    
    def get_param_by_mro(self, clazz, *nodes, **kwargs):
        """
        Returns the configuration parameters. Shortcut to the configurator's get_param_by_mro method
        """
        # Convenient call to the underlying configurator
        return self._configurator.get_param_by_mro(clazz, *nodes, **kwargs)
    
    def shutdown(self):
        """
        Shuts down the domain, effectively shutting down all the services
        """
        while self._service_stack:
            try:
                service = self._service_stack.pop()
                service_clazz = type(service)
                if self._verbose and self.logger:
                    self.logger.info("Shutting down service {}".format(service_clazz.__name__))
                service.shutdown()
            except Exception as e:
                if self.logger:
                    self.logger.exception("Error shutting down service {}: {}".format(service.__class__.__name__, e))
                else:
                    print("Service {} failed to shut down".format(service.__class__.__name__), file=sys.stderr)
                    traceback.print_exc()
    
    def __str__(self) -> str:
        return str(self._configurator)
    
if __name__ == "__main__":
    domain = Domain()
    print(domain)