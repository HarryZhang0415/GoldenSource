import pytest
from unittest.mock import Mock, patch
from GoldenSource.python.utils.patterns import Singleton, cache_result, ReadOnlyDescriptor, TimeIt, BadConfigException


class TestSingleton:
    def test_singleton_meta(self):
        class MyClass(metaclass=Singleton):
            pass

        instance1 = MyClass()
        instance2 = MyClass()

        assert instance1 is instance2


class TestCacheResult:
    def test_cache_result(self):
        @cache_result
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert add(1, 2) == 3
        assert add._results_cache[((1, 2), ())] == 3

        add.reset_cache()
        assert ((1, 2), ()) not in add._results_cache 


class TestReadOnlyDescriptor:
    def test_read_only_descriptor(self):
        class MyClass:
            attr = ReadOnlyDescriptor('attr', ex_type=BadConfigException)

            def parse(self):
                self._attr = 'value'

        instance = MyClass()

        with pytest.raises(BadConfigException):
            _ = instance.attr

        instance.parse()
        assert instance.attr == 'value'

        with pytest.raises(BadConfigException):
            instance.attr = 'new_value'


class TestTimeIt:
    @patch('GoldenSource.python.utils.patterns.time.time', side_effect=[1, 2])
    def test_time_it_with_logger(self, mock_time):
        logger = Mock()
        with TimeIt(logger=logger, tag='Test') as timer:
            pass

        logger.log.assert_any_call('Starting <Test>', level_string='INFO')
        logger.log.assert_any_call('<Test> took 1.000000 seconds', level_string='INFO')
        assert timer.time_elapsed == 1

    @patch('GoldenSource.python.utils.patterns.time.time', side_effect=[1, 2])
    def test_time_it_with_print(self, mock_time):
        with patch('builtins.print') as mock_print:
            with TimeIt(tag='Test') as timer:
                pass

            mock_print.assert_any_call('Starting <Test>')
            mock_print.assert_any_call('<Test> took 1.000000 seconds')
            assert timer.time_elapsed == 1

    @patch('GoldenSource.python.utils.patterns.time.time', side_effect=[1, 2])
    def test_time_it_with_custom_callbacks(self, mock_time):
        on_enter = Mock()
        on_exit = Mock()
        with TimeIt(on_enter=on_enter, on_exit=on_exit) as timer:
            pass

        on_enter.assert_called_once()
        on_exit.assert_called_once_with(1)
        assert timer.time_elapsed == 1
