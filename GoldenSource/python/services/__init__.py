import datetime
import logging
import sys
import os
import traceback


import GS.enums.event as en_evt
import dateutil.parser



from logging.handlers import RotatingFileHandler
from GoldenSource.python.utils import patterns

from GoldenSource.python.utils import camelcase_to_underscore

class Service(object):
    """
    Generic service interface. Services are not required to implement this, but it makes things easier.
    """

    def __init__(self, domain) -> None:
        """
        Invoked upon initialization of the service. This will be called once and once only.
        @type domain: Domain
        @param domain: The active domain
        """
        super(Service, self).__init__()
        pass

    def shutdown(self):
        """
        Invoked when the service is being shut down. This will be called once and once only.
        """
        pass

