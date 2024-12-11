import pytest
from GoldenSource.python.utils.data_types import ndict


def test_ndict_missing_key():
    n = ndict()
    assert isinstance(n['missing_key'], ndict)
    assert 'missing_key' in n


def test_ndict_extract():
    n = ndict()
    n['key1'] = 1
    n['key2']['subkey1'] = 2
    n['key3']['subkey2']['subsubkey1'] = 3
    extracted = n.extract()
    assert extracted == [1, 2, 3]


def test_ndict_extract_all():
    d = {'key1': 1, 'key2': {'subkey1': 2},
         'key3': {'subkey2': {'subsubkey1': 3}}}
    extracted = ndict.extract_all(d)
    assert extracted == [1, 2, 3]


def test_ndict_flatten():
    n = ndict()
    n['key1'] = 1
    n['key2']['subkey1'] = 2
    n['key3']['subkey2']['subsubkey1'] = 3
    flattened = n.flatten()
    assert flattened == {'key1': 1, 'key2_subkey1': 2,
                         'key3_subkey2_subsubkey1': 3}


def test_ndict_flatten_all():
    d = {'key1': 1, 'key2': {'subkey1': 2},
         'key3': {'subkey2': {'subsubkey1': 3}}}
    flattened = ndict.flatten_all(d)
    assert flattened == {'key1': 1, 'key2_subkey1': 2,
                         'key3_subkey2_subsubkey1': 3}
