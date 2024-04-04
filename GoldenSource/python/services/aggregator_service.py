from GoldenSource.python.common.services import Service
from GoldenSource.python.utils import camelcase_to_underscore

class AggregatorService(Service):
    
    """
    Service that aggregates multiple subservices into one.
    The DEFAULT_ROUTING class memeber describe the routing that happens. It should be a dictionary 
    mapping a method_name to its service class.
    The constructor that takes over and adequately creates:
        - methods in the Aggregator that match the child service and simply routes to its corresponding method
        - properties to directly access the inner child services directly
    """
    DEFAULT_ROUTING = {}

    def __init__(self, domain) -> None:
        super(AggregatorService, self).__init__(domain)
        self._routing = domain.get_param(self.__class__.__name__, 'routing', default=self.DEFAULT_ROUTING)

        for service_class in set(self._routing.values()):
            setattr(self, camelcase_to_underscore(service_class.__name__), domain.get_service(service_class))
        
        # Generate the routing
        for method_name, service_class in self._routing.items():
            service = domain.get_service(service_class)
            setattr(self, method_name, getattr(service, method_name))
    