import pytest
import os
from GoldenSource.python.utils.environment import env_get


def test_env_get_existing_variable(monkeypatch):
    monkeypatch.setenv('TEST_VAR', 'test_value')
    assert env_get('TEST_VAR') == 'test_value'


def test_env_get_non_existing_variable():
    assert env_get('NON_EXISTING_VAR') == ''


def test_env_get_with_default():
    assert env_get('NON_EXISTING_VAR',
                   default='default_value') == 'default_value'


def test_env_get_with_conversion(monkeypatch):
    monkeypatch.setenv('TEST_VAR', '123')
    assert env_get('TEST_VAR', as_type=int) == 123


def test_env_get_multiple_variables(monkeypatch):
    monkeypatch.setenv('TEST_VAR1', 'value1')
    monkeypatch.setenv('TEST_VAR2', 'value2')
    assert env_get('NON_EXISTING_VAR', 'TEST_VAR1', 'TEST_VAR2') == 'value1'


def test_env_get_multiple_variables_with_default():
    assert env_get('NON_EXISTING_VAR1', 'NON_EXISTING_VAR2',
                   default='default_value') == 'default_value'
