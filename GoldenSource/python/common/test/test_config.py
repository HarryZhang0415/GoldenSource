import pytest
import datetime
import argparse
import os
import dateutil.parser
from GoldenSource.python.common.config import Configurator
from GoldenSource.python.error.parse import BadConfigException
from GoldenSource.python.utils.patterns import ReadOnlyDescriptor

class DummyConfigurator(Configurator):
    date = ReadOnlyDescriptor("date")

    def __init__(self) -> None:
        super(DummyConfigurator, self).__init__()

        self._parser = argparse.ArgumentParser()
        self._parser.add_argument("--date", metavar="DATE", dest='_date', default=datetime.date.today(), type=self._read_date)

    @staticmethod
    def _read_date(date):
        return dateutil.parser.parse(date).date()

@pytest.fixture
def setup_all_fields():
    return (
        "name",
        "full_name",
        "instance_name",
        "config_path",
        "config_file",
        "core_config_file",
        "log_path",
        "log_to_stdout",
        "local_data_path",
    )

@pytest.fixture
def dval():
    return "bogus value"

def test_no_parse(setup_all_fields, dval):
    cfg_type = Configurator
    cfg = Configurator()

    for field in setup_all_fields:
        with pytest.raises(BadConfigException):
            cfg_type.__dict__[field].__get__(cfg, cfg_type)
        with pytest.raises(BadConfigException):
            getattr(cfg, field)

    with pytest.raises(BadConfigException):
        cfg.get_param("Ice")
    with pytest.raises(BadConfigException):
        cfg.__getitem__("Ice")

    for field in setup_all_fields:
        with pytest.raises(BadConfigException):
            cfg_type.__dict__[field].__set__(cfg, dval)
        with pytest.raises(BadConfigException):
            setattr(cfg, field, dval)

def test_parse_no_args(setup_all_fields, dval):
    cfg_type = Configurator
    cfg = Configurator().parse([])

    assert cfg.name == ""
    assert cfg.full_name == ""
    assert cfg.instance_name == ""
    assert cfg.config_file == ""
    assert cfg.log_path == Configurator.DEFAULT_LOG_PATH
    assert not cfg.extra

    assert cfg.get_param("Ice")
    assert cfg.get_param("Ice", "Ice.Default.Locator")
    assert cfg.get_param("Ice") == cfg["Ice"]
    assert cfg.get_param("Ice", "Ice.Default.Locator") == cfg["Ice", "Ice.Default.Locator"]

    assert isinstance(cfg.get_param("Ice", "Ice.Trace.Protocol", as_type=int), int)

    assert cfg.get_param("some", "non-existing", "param") == ""
    assert cfg.get_param("some", "non-existing", "param", default={}) == {}
    assert cfg.get_param("some", "non-existing", "param", default=123456) == 123456

    for field in setup_all_fields:
        with pytest.raises(BadConfigException):
            cfg_type.__dict__[field].__set__(cfg, dval)
        with pytest.raises(BadConfigException):
            setattr(cfg, field, dval)

def test_parse_with_args(setup_all_fields, dval):
    cfg_type = Configurator
    cfg = Configurator().parse(["-n", "some_app"])

    assert cfg.name == "some_app"
    assert cfg.instance_name == ""
    assert cfg.full_name == "some_app"

    assert cfg.get_param("Ice")
    assert cfg.get_param("Ice", "Ice.Default.Locator")
    assert cfg.get_param("Ice") == cfg["Ice"]
    assert cfg.get_param("Ice", "Ice.Default.Locator") == cfg["Ice", "Ice.Default.Locator"]

    assert cfg.get_param("app")
    assert cfg.get_param("app") == cfg["app"]

    assert isinstance(cfg.get_param("Ice", "Ice.Trace.Protocol", as_type=int), int)

    assert cfg.get_param("some", "non-existing", "param") == ""
    assert cfg.get_param("some", "non-existing", "param", default={}) == {}
    assert cfg.get_param("some", "non-existing", "param", default=123456) == 123456

    for field in setup_all_fields:
        with pytest.raises(BadConfigException):
            cfg_type.__dict__[field].__set__(cfg, dval)
        with pytest.raises(BadConfigException):
            setattr(cfg, field, dval)

def test_path_changes():
    cfg1 = Configurator().parse([])
    assert cfg1.config_path == Configurator.DEFAULT_CONFIG_PATH
    assert cfg1.log_path == Configurator.DEFAULT_LOG_PATH
    assert cfg1.local_data_path == Configurator.DEFAULT_LOCAL_DATA_PATH

    cfg2 = Configurator().parse(["--home-path=/root/build/GoldenSource/"])
    home_path = os.environ.get("PROJECT_BUILD_DIR")
    assert cfg2.config_path == os.path.join(home_path, "cfg")
    assert cfg2.log_path == os.path.join(home_path, "log")
    assert cfg2.local_data_path == os.path.join(home_path, "data")

def test_config_override():
    cfg = DummyConfigurator().parse([])
    assert cfg.date == datetime.date.today()
    assert cfg.config_path == Configurator.DEFAULT_CONFIG_PATH
    assert cfg.log_path == Configurator.DEFAULT_LOG_PATH
    assert cfg.local_data_path == Configurator.DEFAULT_LOCAL_DATA_PATH

    cfg = DummyConfigurator().parse(["--date=20240311"])
    assert cfg.date == datetime.date(2024, 3, 11)
    assert cfg.config_path == Configurator.DEFAULT_CONFIG_PATH
    assert cfg.log_path == Configurator.DEFAULT_LOG_PATH
    assert cfg.local_data_path == Configurator.DEFAULT_LOCAL_DATA_PATH
