import os
import sys
import threading

from GoldenSource.python.common.domain import Domain
from GoldenSource.python.common.config import Configurator
from GoldenSource.python.common.application import Application
from GoldenSource.python.services.logger_service import LoggerService
from GoldenSource.python.ice.overrides import override_str_repr



class Runner(object):
    """
    Common entry point for all GoldenSource applications. The Runner is responsible for initializing the application
    It will use the following classes:
        - config.Configurator to parse the command line arguments and the configuration file
        - services.LoggerService to log the messages

    Any applications willing to define a bespoke Configurator or LoggerService would need to either override the class(es) or extend the Runner class
    """

    domain_class = Domain
    configurator_class = Configurator
    logger_class = LoggerService

    def __init__(self) -> None:
        """
        Initializes the Runner, effectively initializing the Domain
        """

        self.domain = self.domain_class(self.configurator_class, self.logger_class)
        self.domain.main_thread = threading.current_thread()

        self.logger = self.domain.get_service(self.logger_class).get_logger(self.__class__.__name__)
        self.app_class = None
        self.app = None
        self.shutdown_called = False

    def run(self):
        """
        Runs the application
        """
        try:
            self.logger.info("---------------------------------------8<---------------------------------------")
            self.logger.info("Starting application {}".format(self.__class__.__name__))
            self.logger.info("With python path: \n{}".format("\n".join(sys.path)))
            self.logger.info("With config:\n{}".format(str(self.domain)))

            # Out of conveniency, override the Ice objects default __str__ and __repr__ methods
            override_str_repr()

            self.app_class = self.domain.get_param("app", "run_class", default=Application)

            self.logger.info("Initializing application {}".format(self.app_class.__name__))
            self.app = self.app_class(self.domain)
            if not self.shutdown_called:
                self.logger.info("Running application {}".format(self.app_class.__name__))
                self.app.run()
            else:
                self.logger.error("Application {} was shutdown before it could run".format(self.app_class.__name__))
        except:
            self.logger.exception("An exception occurred while running the application")
            raise
        finally:
            self.logger.info("Shutting down application {}".format(self.__class__.__name__))
            self.shutdown()

    def shutdown(self):
        """
        Shutdown the runner, effectively shutting down the Domain and the application
        """    
        self.domain.shutdown()
        if self.app is not None and hasattr(self.app, "shutdown"):
            self.logger.info("Shutting down application {}".format(self.app.__class__.__name__))
            self.app.shutdown()

if __name__ == "__main__":
    runner = Runner()
    runner.run()