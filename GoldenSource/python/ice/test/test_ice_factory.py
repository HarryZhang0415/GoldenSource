import pytest
from datetime import datetime, date
from GoldenSource.python.ice.ice_factory import *
import pandas

def test_date_to_idate():
    idate = make_idate(date(2015, 1, 1))
    assert idate.yyyyMMdd == 20150101
    assert idate2date(idate) == date(2015, 1, 1)
    
def test_datetime_to_idate():
    idate = make_idate(datetime(2015, 1, 1, 12, 0, 0))
    assert idate.yyyyMMdd == 20150101
    assert idate2date(idate) == date(2015, 1, 1)

def test_pandas_timestamp_to_idate():
    idate = make_idate(pandas.Timestamp('2015-01-01'))
    assert idate.yyyyMMdd == 20150101
    assert idate2date(idate) == date(2015, 1, 1)

def test_idatetime_to_idate():
    idate = make_idate(IDateTime(0))
    assert idate.yyyyMMdd == 19700101
    assert idate2date(idate) == date(1970, 1, 1)

def test_datetime_to_idatetime():
    idt = datetime_to_idatetime(datetime(2015, 1, 1, 12, 0, 0))
    assert idt.val == 1420113600000000

def test_none_to_idate():
    idate = make_idate(None)
    assert idate is not None

def test_invalid_string_to_idate():
    with pytest.raises(ValueError):
        make_idate("invalid-date")

def test_none_to_idatetime():
    idt = make_idatetime(None)
    assert idt is not None

def test_invalid_string_to_idatetime():
    with pytest.raises(UnboundLocalError):
        make_idatetime("invalid-datetime")

def test_idate_to_idate():
    original_idate = IDate(20220101)
    idate = make_idate(original_idate)
    assert idate.yyyyMMdd == 20220101

def test_idatetime_to_idatetime():
    original_idt = IDateTime(0)
    idt = make_idatetime(original_idt)
    assert idt.val == 0