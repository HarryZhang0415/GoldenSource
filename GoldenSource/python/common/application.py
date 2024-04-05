import os
from GoldenSource.python.common.services import Service
from GoldenSource.python.error.parse import BadConfigException


class Application(Service):
    def __init__(self, domain) -> None:
        super(Application, self).__init__(domain)
        self.domain = domain
        self.app_name = self.domain.get_param("app", "full_name")
        self.app_pid = os.getpid()
        self.logger_service = self.domain.logger_service
        self.logger = self.logger_service.get_logger(self.__class__.__name__)

    def run(self):
        raise BadConfigException("app.run_class must be specified in the configuration file in order to use the Runner")