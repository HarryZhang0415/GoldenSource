import unittest
from GoldenSource.python.ice.ice_factory import *

class IDateTest(unittest.TestCase):
    def test_date_to_idate(self):
        idate = make_idate(date(2015, 1, 1))
        self.assertEqual(idate.yyyyMMdd, 20150101)
        self.assertEqual(idate2date(idate), date(2015, 1, 1))
    
    def test_datetime_to_idate(self):
        idate = make_idate(datetime(2015, 1, 1, 12, 0, 0))
        self.assertEqual(idate.yyyyMMdd, 20150101)
        self.assertEqual(idate2date(idate), date(2015, 1, 1))

    def test_pandas_timestamp_to_idate(self):
        idate = make_idate(pandas.Timestamp('2015-01-01'))
        self.assertEqual(idate.yyyyMMdd, 20150101)
        self.assertEqual(idate2date(idate), date(2015, 1, 1))

    def test_idatetime_to_idate(self):
        idate = make_idate(IDateTime(0))
        self.assertEqual(idate.yyyyMMdd, 19700101)
        self.assertEqual(idate2date(idate), date(1970, 1, 1))

    def test_datetime_to_idatetime(self):
        idt = datetime_to_idatetime(datetime(2015, 1, 1, 12, 0, 0))
        self.assertEqual(idt.val, 1420113600000000)

if __name__ == "__main__":
    unittest.main()