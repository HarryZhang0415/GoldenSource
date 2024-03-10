import argparse
import os
import types
import sys
import pickle
from os.path import normpath, expanduser, expandvars, join, exists

from quant.utils.data_types import ndict
from quant.utils.patterns import ReadOnlyDescriptor


class ConfigurationError(Exception):
    """
    Raised when the Configurator encounters an error
    """

class Configurator(object):
    name = ReadOnlyDescriptor("name")
    full_name = ReadOnlyDescriptor("full_name")
    instance_name = ReadOnlyDescriptor("instance_name")
    extra = ReadOnlyDescriptor("extra")
    config = ReadOnlyDescriptor("config")
    config_path = ReadOnlyDescriptor("config_path")
    config_file = ReadOnlyDescriptor("config_file")
    core_config_file = ReadOnlyDescriptor("core_config_file")
    log_path = ReadOnlyDescriptor("log_path")
    log_to_stdout = ReadOnlyDescriptor("log_to_stdout")
    local_data_path = ReadOnlyDescriptor("local_data_path")
    home_path = ReadOnlyDescriptor("home_path")
    pricing_environment = ReadOnlyDescriptor("pricing_environment")
    
    disable_hb = ReadOnlyDescriptor("disable_hb")
    hb_interval = ReadOnlyDescriptor("hb_interval")

    keys_to_remove = ("__builtins__",)
    value_types_to_remove = (types.ModuleType, type)

    
