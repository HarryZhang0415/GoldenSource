import unittest
import datetime
import argparse
import os

import dateutil.parser

from GoldenSource.common.config import Configurator
from GoldenSource.error.parse import BadConfigException
from GoldenSource.utils.patterns import ReadOnlyDescriptor

class DummyConfigurator(Configurator):
    date = ReadOnlyDescriptor("date")

    def __init__(self) -> None:
        super(DummyConfigurator, self).__init__()

        self._parser = argparse.ArgumentParser()
        self._parser.add_argument("--date", metavar="DATE", dest='_date', default=datetime.date.today(), type=self._read_date)

    @staticmethod
    def _read_date(date):
        return dateutil.parser.parse(date).date()
    
class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.all_fields = (
            "name"
            , "full_name"
            , "instance_name"
            , "config_path"
            , "config_file"
            , "core_config_file"
            , "log_path"
            , "log_to_stdout"
            , "local_data_path"
        )
        self.dval = "bogus value"

    def test_no_parse(self):
        """
        Makes sure any access to the configurator without prior call to parse() fails
        """
        cfg_type = Configurator
        cfg = Configurator()

        # No fields shoudl be accessible without raising an exception
        # 2 ways of accessing the fields
        for field in self.all_fields:
            self.assertRaises(BadConfigException, cfg_type.__dict__[field].__get__, cfg, cfg_type)
            self.assertRaises(BadConfigException, getattr, cfg, field)

        # No parameter should be readable at this point
        self.assertRaises(BadConfigException, cfg.get_param, "Ice")
        self.assertRaises(BadConfigException, cfg.__getitem__, "Ice")

        # All fields should be readonly
        for field in self.all_fields:
            self.assertRaises(ValueError, cfg_type.__dict__[field].__set__, cfg, self.dval)
            self.assertRaises(ValueError, setattr, cfg, field, self.dval)

    def test_parse_no_args(self):
        """
        Ensures the most basic configurator setup works as expected
        """
        cfg_type = Configurator
        cfg = Configurator().parse([])

        # All fields default to an empty string/array
        self.assertEqual(cfg.name, "")
        self.assertEqual(cfg.full_name, "")
        self.assertEqual(cfg.instance_name, "")
        self.assertEqual(cfg.config_file, "")
        self.assertEqual(cfg.log_path, Configurator.DEFAULT_LOG_PATH)
        self.assertFalse(cfg.extra)

        # ctpcore.cfg should be properly loaded
        self.assertTrue(cfg.get_param("Ice"))
        self.assertTrue(cfg.get_param("Ice", "Ice.Default.Locator"))
        self.assertDictEqual(cfg.get_param("Ice"), cfg["Ice"])
        self.assertEqual(cfg.get_param("Ice", "Ice.Default.Locator"), cfg["Ice", "Ice.Default.Locator"])

        # Makes sure the get_param() switches work as intended
        # Test the as_type switch
        self.assertIs(type(cfg.get_param("Ice", "Ice.Trace.Protocol", as_type=int)), int)
        
        self.assertEqual(cfg.get_param("some", "non-existing", "param"), "")
        self.assertEqual(cfg.get_param("some", "non-existing", "param", default={}), {})
        self.assertEqual(cfg.get_param("some", "non-existing", "param", default=123456), 123456)

        # All fields should be readonly
        # 2 ways of setting the fields
        for field in self.all_fields:
            self.assertRaises(ValueError, cfg_type.__dict__[field].__set__, cfg, self.dval)
            self.assertRaises(ValueError, setattr, cfg, field, self.dval)

    def test_parse_with_args(self):
        """
        Ensures a given servant setup works as expected
        """
        cfg_type = Configurator
        cfg = Configurator().parse(["-n", "some_app"])

        # The fields should be initialized
        self.assertEqual(cfg.name, "some_app")
        self.assertEqual(cfg.instance_name, "")
        self.assertEqual(cfg.full_name, "some_app")

        #ctpcore.cfg should be prperly loaded
        self.assertTrue(cfg.get_param("Ice"))
        self.assertTrue(cfg.get_param("Ice", "Ice.Default.Locator"))
        self.assertDictEqual(cfg.get_param("Ice"), cfg["Ice"])
        self.assertEqual(cfg.get_param("Ice", "Ice.Default.Locator"), cfg["Ice", "Ice.Default.Locator"])

        # references.cfg should be loaded as well
        self.assertTrue(cfg.get_param("app"))
        self.assertDictEqual(cfg.get_param("app"), cfg["app"])
        self.assertDictEqual(cfg.get_param("app",), cfg["app"])

        # Makes sure the get_param() switches work as intended
        # Test the as_type switch
        self.assertIs(type(cfg.get_param("Ice", "Ice.Trace.Protocol", as_type=int)), int)

        # Test the default switch
        self.assertEqual(cfg.get_param("some", "non-existing", "param"), "")
        self.assertEqual(cfg.get_param("some", "non-existing", "param", default={}), {})
        self.assertEqual(cfg.get_param("some", "non-existing", "param", default=123456), 123456)

        # All should be readonly
        # 2 ways of setting the fields
        for field in self.all_fields:
            self.assertRaises(ValueError, cfg_type.__dict__[field].__set__, cfg, self.dval)
            self.assertRaises(ValueError, setattr, cfg, field, self.dval)

    def test_path_changes(self):
        cfg1 = Configurator().parse([])
        self.assertEqual(cfg1.config_path, Configurator.DEFAULT_CONFIG_PATH)
        self.assertEqual(cfg1.log_path, Configurator.DEFAULT_LOG_PATH)
        self.assertEqual(cfg1.local_data_path, Configurator.DEFAULT_LOCAL_DATA_PATH)
        
        cfg2 = Configurator().parse(["--home-path=/root/build/GoldenSource/"])
        home_path = os.environ.get("PROJECT_BUILD_DIR")
        self.assertEqual(cfg2.config_path, os.path.join(home_path, "cfg"))
        self.assertEqual(cfg2.log_path, os.path.join(home_path, "log"))
        self.assertEqual(cfg2.local_data_path, os.path.join(home_path, "data"))

    def test_config_override(self):
        cfg = DummyConfigurator().parse([])
        self.assertEqual(cfg.date, datetime.date.today())
        self.assertEqual(cfg.config_path, Configurator.DEFAULT_CONFIG_PATH)
        self.assertEqual(cfg.log_path, Configurator.DEFAULT_LOG_PATH)
        self.assertEqual(cfg.local_data_path, Configurator.DEFAULT_LOCAL_DATA_PATH)

        cfg = DummyConfigurator().parse(['--date=20240311'])
        self.assertEqual(cfg.date, datetime.date(2024,3,11))
        self.assertEqual(cfg.config_path, Configurator.DEFAULT_CONFIG_PATH)
        self.assertEqual(cfg.log_path, Configurator.DEFAULT_LOG_PATH)
        self.assertEqual(cfg.local_data_path, Configurator.DEFAULT_LOCAL_DATA_PATH)

if __name__ == "__main__":
    unittest.main()