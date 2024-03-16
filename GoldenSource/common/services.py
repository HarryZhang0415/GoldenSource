import datetime
import logging
import sys
import traceback

import GS.dataobjects as do;
import GS.dataobjects.event as do_evt
import GS.enums.event as en_evt
import dateutil.parser

from logging.handlers import RotatingFileHandler
from GoldenSource.utils import patterns
from GoldenSource.utils import convert 