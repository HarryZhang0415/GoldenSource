import argparse
import os
import types
import sys
import pickle
from os.path import normpath, expanduser, expandvars, join, exists

from quant.utils.data_types import ndict
from quant.utils.patterns import ReadOnlyDescriptor
from quant.utils.environment import env_get


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

    DEFAULT_ROOT_PATH = os.getenv("PROJECT_SRC_DIR")
    DEFAULT_CONFIG_PATH = join(DEFAULT_ROOT_PATH, "cfg")
    DEFAULT_LOG_PATH    = join(DEFAULT_ROOT_PATH, "log")
    DEFAULT_LOCAL_DATA_PATH = join(DEFAULT_ROOT_PATH, "data")
    DEFAULT_CORE_CONFIG_FILE = "core.cfg"

    @classmethod
    def set_default_root_path(cls, path):
        cls.DEFAULT_ROOT_PATH = expandvars(expanduser(normpath(path)))
        cls.DEFAULT_CONFIG_PATH = join(cls.DEFAULT_ROOT_PATH, 'etc')
        cls.DEFAULT_LOG_PATH = join(cls.DEFAULT_ROOT_PATH, 'log')
        cls.DEFAULT_LOCAL_DATA_PATH = join(cls.DEFAULT_ROOT_PATH, 'data')

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(description='Configurator Command Line Parser')
        self._parser.add_argument("-n", "--name", metavar="NAME", dest="_name", default="", type=str, help="app name")
        self._parser.add_argument("-i", "--instance-name", metavar="INSTANCE", dest="_instance_name", default="", type=str, help="app instance name")
        self._parser.add_argument("-c", "--config-path", metavar="CONFIG_PATH", dest="_config_path", default="", type=str)
        self._parser.add_argument("--config-file", metavar="CONFIG_FILE", dest="_config_file", default="", type=str)
        self._parser.add_argument("--core-config-file", metavar="CORE_CONFIG_FILE", dest="_core_config_file", default="", type=str)
        self._parser.add_argument("-l", "--log-file-path", metavar="LOG", dest="_log_path", default="", type=str)
        self._parser.add_argument("-log-to-stdout", "_log_to_stdout", default=False, action="store_true")
        self._parser.add_argument("--home-path", metavar="PATH", dest="_home_path", default="", type=str)
        self._parser.add_argument("--pricing-environment", metavar="ENV", dest='_pricing_environment', default="", type=str)
        self._parser.add_argument("_extra", metavar="EXTRA", nargs="*")


        # Heartbeat commands:
        self._parser.add_argument("--disable-hb", dest="_disable_hb", action="store_true")
        self._parser.add_argument("--hb-interval", dest='_hb_interval', type=int, default=120)

        self._args = None
        self._defaults = {
            "_name": ""
            , "_full_name": ""
            , "_instance_name": ""
            , "_config_path": ""
            , "_config_file": ""
            , "_core_config_file": ""
            , "_log_path": ""
            , "_log_to_stdout": False
            , "_local_data_path": ""
            , "_home_path": ""
            , "_pricing_environment": ""
            , "_extra": []
            , "_disable_hb": False
            , "_interval": 120
        }

    def _default(self):
        for item, default in self._defaults.items():
            if not hasattr(self, item):
                setattr(self, item, default)

    def parse(self, args=None, fail_on_err=True):
        try:
            self._args = args if args is not None else sys.argv[1:]
            self._parser.parse_args(self._args, namespace=self)
        except:
            if fail_on_err:
                raise

        self._default()
        self._parse_config()
        return self
    
    def __getitem__(self, k):
        """
        Returns the parameter value for the node(s).
        These calls are equivalent:
            1) cfg[a] == get_param(a)
            2) cfg[a, b, c] == get_param(a, b, c)

        Arguments:
        - nodes The node names pointing at the parameter to retrieve
        """
        if isinstance(k, (tuple, list, set, dict)):
            return self.get_param(*k)
        else:
            return self.get_param(k)
        
    def get_param(self, *nodes, **kwargs):
        """
        Returns the parameter value for the nodes.

        Arguments:
        - nodes: The node names pointing at the parameter to retrieve
        Additional arguments: (these need to be explicitely defined, e.g. default=xxx)
        - default: The value returned if no parameter is found, defaults to an empty string
        - as_type: On-the-fly conversion of the parameter, needs to be callable. 
                    This will *not* be applied to the default value.
        """

        cd = self.config
        for k in nodes:
            if k in cd:
                cd = cd[k]
            else:
                return kwargs.get("default", "")
        
        as_type = kwargs.get("as_type")
        if as_type is not None:
            assert callable(as_type), "as_type must be callable"
            return as_type(cd)
        else:
            return cd
    
    def get_param_by_mro(self, clazz, *nodes, **kwargs):
        """
        Returns the parameter value for the nodes, following the mro of the class passed as an argument
        
        Arguments:
        - clazz: The clazz to reverse follow the mro for
        - nodes: the node names pointing at the parameter to retrieve
        Additional arguments: (these need to be explicitely defined, e.g. default=XXX)
        - default: the value returned if no paramter is found, defaults to an empty string
        - as_type: On-The-fly conversion of the parameter, needs to be callable. 
                    This will *not* be applied to the default value.
        """
        value = kwargs.get('default', '')
        if clazz in reversed(clazz.__mro__):
            value = self.get_param(clazz.__name__, *nodes, **kwargs)
            kwargs['default'] = value

        return value
    
    def _execfile(input, overrides):
        with open(input) as f:
            code = compile(f.read(), input, 'exec')
            exec(code, overrides)
        
    def _parse_config(self):
        """
        Parses the configuration based on the command line switches, if any.
        """
        self._config = ndict()

        # Read and define the main arguments
        self._full_name = self.name
        if self.instance_name:
            self._full_name += ".{}".format(self.instance_name)
        
        if self.home_path:
            self.set_default_root_path(self.home_path)
        else:
            self._home_path = self.DEFAULT_ROOT_PATH
        
        if not self.config_path:
            self._config_path = self.DEFAULT_CONFIG_PATH
        self._config_path = expanduser(self._config_path)
        if not self.config_file and self.name:
            self._config_file = join(self.config_path, '{name}.cfg'.format(name=self.name))
        self._config_file = expanduser(self._config_file)
        if not self.core_config_file:
            self._core_config_file = join(self.config_path, self.DEFAULT_CORE_CONFIG_FILE)
        self._core_config_file = expanduser(self._core_config_file)
        if not self.log_path:
            self._log_path = self.DEFAULT_LOG_PATH
        self._log_path = expanduser(self._log_path)
        if not self.local_data_path:
            self._local_data_path = self.DEFAULT_LOCAL_DATA_PATH
        self._local_data_path = expanduser(self._local_data_path)
        log_file = ""
        if self.full_name:
            log_file = join(self.log_path, '{name}.log'.format(name=self.full_name))
        
        self._config["app"]["name"] = self.name
        self._config["app"]["full_name"] = self.full_name
        self._config["app"]["config_path"] = self.config_path
        self._config["app"]["config_file"] = self.config_file
        self._config["app"]["core_config_file"] = self.core_config_file
        self._config["app"]["log_file_path"] = log_file
        self._config["app"]["log_to_stdout"] = self.log_to_stdout
        self._config["app"]["pricing_environment"] = self.pricing_environment

        # Read the core config file
        core_config = {}
        self._execfile(self.config_file, core_config)
        self._apply_config_overrides(self._config, core_config)

        overrides = {}
        if self.config_file and exists(self.config_file):
            sys_args = sys.argv
            sys.argv = ["--core-config-file={}".format(self.core_config_file)]
            if self.log_to_stdout:
                sys.argv.append("--log-to-stdout")
            self._execfile(self.config_file, overrides)
            sys.argv = sys_args
        
        # Apply the overrides
        self._apply_config_overrides(self._config, overrides)

        try:
            db_dict = pickle.load(open(self._config['db_config']['pickle_file_location'], 'rb'))
            self._apply_config_overrides(self._config, db_dict)
        except:
            pass

        pricing_overrides = {}
        if not self.pricing_environment:
            self._pricing_environment = self.get_param("pricing_environment_name")
        if self.pricing_environment:
            pricing_env_file = join(self.config_path, 'pricing_environment.{}.cfg'.format(self.pricing_environment))
            if exists(pricing_env_file):
                self._execfile(pricing_env_file, pricing_overrides)
        
        self._apply_config_overrides(self._config, pricing_overrides)

        # Doing cleanup
        self._config = self._cleanup_config(self._config)
        if self.full_name:
            ice_cfg = self.get_param("Ice")
            ice_cfg.setdefault("Ice.ProgramName", self.full_name)

    @staticmethod
    def _apply_config_overrides(originals, overrides, key_prefix=''):
        for key, override_value in overrides.items():
            original_value = originals.get(key)
            if override_value is None:
                originals[key] = None
            elif isinstance(override_value, dict):
                # Override with a dictionary, perform a few checks and recursively override the values
                if original_value is None:
                    original_value = {}
                    originals[key] = original_value
                elif not isinstance(original_value, dict):
                    raise ConfigurationError("{}{}: expected {}, got dict instead ".format(key_prefix, key, original_value.__class__.__name__))
                Configurator._apply_config_overrides(original_value, override_value, key_prefix='{}{}.'.format(key_prefix, key))
            else:
                # override the value with any other value, provided we are not about to trample a dict
                if isinstance(original_value, dict):
                    raise ConfigurationError("{}{}: expected dict, got {} instead ".format(key_prefix, key, override_value.__class__.__name__))
                originals[key] = override_value
    
    def _cleanup_config(self, config):
        return ndict({
            k: v for k, v in config.items()
            if k not in self.keys_to_remove and type(v) not in self.value_types_to_remove
        })
    
    @staticmethod
    def param_to_str(param, value, indent=0):
        """
        Utility function to pretty print the Domain parameters, properly indented for clarity
        : param: The parameter key
        : value: The value
        : indent: The indentation
        """
        s = ""
        if isinstance(value, dict):
            s += "\t" * indent + str(param) + " {\n"
            for p in value.keys():
                s += Configurator.param_to_str(p, value[p], indent + 1)
            s += "\\t" * indent + "} // " + str(param) + "\n"
        else:
            s += "\t" * indent + "{} -> {}\n".format(param, value)
        return s
    
    def __str__(self):
        s = ""
        for param, value in sorted(((k, v) for k, v in vars(self).items() if k not in ("_config", "_defaults", "_parser")), key=lambda t: t[0]):
            s += self.param_to_str(param, value)
        for param, value in self._config.items():
            s += self.param_to_str(param, value)
        return s
    
    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._args)
    

class LocalConfigurator(Configurator):
    """
    Configurator that defaults to $HOME/etc.log.data if defined.
    """
LocalConfigurator.set_default_root_path(env_get('PROJECT_SRC_DIR', 'PROJECT_BUILD_DIR', default=join('~', 'root')))

class NoArgsConfigurator(Configurator):
    """
    Configurator that never parses the command line arguments
    """

    def parse(self, args=None, fail_on_err=True):
        return super(NoArgsConfigurator, self).parse([], fail_on_err)

class LocalNoArgsConfigurator(LocalConfigurator, NoArgsConfigurator):
    pass

class LocalNoRedirectConfigurator(LocalConfigurator):
    def parse(self, args=None, fail_on_error=True):
        super(LocalNoRedirectConfigurator, self).parse([], fail_on_error)
        self._config["logger"]['redirect_stdout'] = False
        self._config["logger"]["redirect_stderr"] = False
        return self