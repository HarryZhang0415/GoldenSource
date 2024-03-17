from datetime import datetime, timedelta, date
import unittest

import GS.dataobjects as do
import GS.dataobjects.reference as do_ref

from GoldenSource.common.domain import Domain
from GoldenSource.common.services import TimeService
from GoldenSource.ice import ice_factory


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.day_offset = timedelta(1)
        self.time = Domain().get_service(TimeService)
        self.time.set_reference_date(date(2014, 7, 6))
        cal = do_ref.Calendar()
        cal.holidays = {
            ice_factory.make_idate('2014-06-26'): None
            , ice_factory.make_idate('2014-07-03'): None
            , ice_factory.make_idate('2014-07-04'): None
            , ice_factory.make_idate('2014-07-05'): None
            , ice_factory.make_idate('2014-07-07'): None
        }
        self.time.set_calendar(cal)

    def test_reference_dates(self):
        self.assertEqual(self.time.reference_date(), date(2014, 7, 6))
        self.assertEqual(self.time.today(), date(2014, 7, 6))
        self.assertEqual(self.time.yesterday(), date(2014, 7, 5))
        self.assertEqual(self.time.today(as_business_day=True), date(2014, 7, 2))
        self.assertEqual(self.time.yesterday(as_business_day=True), date(2014, 7, 2))

    def test_conversions(self):
        self.assertEqual(self.time.today(as_type=date), self.time.today())
        self.assertEqual(self.time.today(as_type=datetime), datetime(2014, 7, 6))
        self.assertEqual(self.time.today(as_type=str), '2014-07-06')
        self.assertEqual(self.time.today(as_type=do.IDate).yyyyMMdd, 20140706)
        self.assertEqual(self.time.today(as_type=int), 20140706)
        self.assertEqual(self.time.today(as_type=tuple), None)

        epoch = datetime(1970, 1, 1)

        one_second = timedelta(seconds=1)
        self.assertAlmostEqual(self.time.now(as_type=datetime), self.time.now(), delta=one_second)
        self.assertAlmostEqual(self.time.now(as_type=datetime), datetime.combine(date(2014, 7, 6), datetime.now().time()), delta=one_second)
        self.assertEqual(self.time.now(as_type=do.IDate).yyyyMMdd, 20140706)
        self.assertEqual(self.time.now(as_type=str)[:18], datetime.combine(date(2014, 7, 6), datetime.now().time()).isoformat()[:18])
        self.assertAlmostEqual(self.time.now(as_type=int) / 1000000, int((datetime.combine(date(2014, 7, 6), datetime.now().time()) - epoch).total_seconds()), delta=1)
        self.assertAlmostEqual(self.time.now(as_type=tuple), None)

    def test_readings(self):
        self.assertEqual(self.time.read_date(self.time.reference_date()), self.time.reference_date())
        self.assertEqual(self.time.read_date(self.time.reference_date(as_type=date)), self.time.reference_date())
        self.assertEqual(self.time.read_date(self.time.reference_date(as_type=datetime)), self.time.reference_date())
        self.assertEqual(self.time.read_date(self.time.reference_date(as_type=do.IDate)), self.time.reference_date())
        self.assertEqual(self.time.read_date(self.time.reference_date(as_type=str)), self.time.reference_date())
        self.assertEqual(self.time.read_date(self.time.reference_date(as_type=int)), self.time.reference_date())

    def test_calendar_offsets(self):
        self.assertEqual(self.time.next_day(), self.time.today())
        self.assertEqual(self.time.next_day(offset=-1), self.time.yesterday())
        self.assertEqual(self.time.next_day(offset=-2), date(2014, 7, 4))
        self.assertEqual(self.time.next_day(offset=-3), date(2014, 7, 3))
        self.assertEqual(self.time.next_day(offset=-11), date(2014, 6, 25))
        self.assertEqual(self.time.next_day(offset=-27), date(2014, 6, 9))
        self.assertEqual(self.time.next_day(offset=1), date(2014, 7, 7))
        self.assertEqual(self.time.next_day(offset=2), date(2014, 7, 8))
        self.assertEqual(self.time.next_day(offset=3), date(2014, 7, 9))
        self.assertEqual(self.time.next_day(offset=11), date(2014, 7, 17))
        self.assertEqual(self.time.next_day(offset=27), date(2014, 8, 2))

    def test_nearest_business_offsets(self):
        self.assertEqual(self.time.next_day(as_business_day=True), self.time.today(as_business_day=True))
        self.assertEqual(self.time.next_day(offset=-1, as_business_day=True), self.time.yesterday(as_business_day=True))
        self.assertEqual(self.time.next_day(offset=-2, as_business_day=True), date(2014, 7, 2))
        self.assertEqual(self.time.next_day(offset=-3, as_business_day=True), date(2014, 7, 2))
        self.assertEqual(self.time.next_day(offset=-11, as_business_day=True), date(2014, 6, 25))
        self.assertEqual(self.time.next_day(offset=-27, as_business_day=True), date(2014, 6, 9))
        self.assertEqual(self.time.next_day(offset=1, as_business_day=True), date(2014, 7, 2))
        self.assertEqual(self.time.next_day(offset=2, as_business_day=True), date(2014, 7, 8))
        self.assertEqual(self.time.next_day(offset=3, as_business_day=True), date(2014, 7, 9))
        self.assertEqual(self.time.next_day(offset=11, as_business_day=True), date(2014, 7, 17))
        self.assertEqual(self.time.next_day(offset=27, as_business_day=True), date(2014, 8, 1))

    def test_business_offsets(self):
        self.assertEqual(self.time.next_business_day(offset=0), self.time.today(as_business_day=True))
        self.assertEqual(self.time.next_business_day(offset=-1), date(2014, 7, 1))
        self.assertEqual(self.time.next_business_day(offset=-2), date(2014, 6, 30))
        self.assertEqual(self.time.next_business_day(offset=-3), date(2014, 6, 27))
        self.assertEqual(self.time.next_business_day(offset=-11), date(2014, 6, 16))
        self.assertEqual(self.time.next_business_day(offset=-27), date(2014, 5, 23))
        self.assertEqual(self.time.next_business_day(offset=1), date(2014, 7, 8))
        self.assertEqual(self.time.next_business_day(offset=2), date(2014, 7, 9))
        self.assertEqual(self.time.next_business_day(offset=3), date(2014, 7, 10))
        self.assertEqual(self.time.next_business_day(offset=11), date(2014, 7, 22))
        self.assertEqual(self.time.next_business_day(offset=27), date(2014, 8, 13))

    def test_reverse_offsets(self):
        self.assertEqual(self.time.next_day(offset=-1, reverse=True), self.time.next_day(offset=1))
        self.assertEqual(self.time.next_day(offset=-2, reverse=True), self.time.next_day(offset=2))
        self.assertEqual(self.time.next_day(offset=-3, reverse=True), self.time.next_day(offset=3))
        self.assertEqual(self.time.next_day(offset=-11, reverse=True), self.time.next_day(offset=11))
        self.assertEqual(self.time.next_day(offset=-27, reverse=True), self.time.next_day(offset=27))
        self.assertEqual(self.time.next_day(offset=1, reverse=True), self.time.next_day(offset=-1))
        self.assertEqual(self.time.next_day(offset=2, reverse=True), self.time.next_day(offset=-2))
        self.assertEqual(self.time.next_day(offset=3, reverse=True), self.time.next_day(offset=-3))
        self.assertEqual(self.time.next_day(offset=11, reverse=True), self.time.next_day(offset=-11))
        self.assertEqual(self.time.next_day(offset=27, reverse=True), self.time.next_day(offset=-27))

        self.assertEqual(self.time.next_day(offset=-1, reverse=True, as_business_day=True), self.time.next_day(offset=1, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=-2, reverse=True, as_business_day=True), self.time.next_day(offset=2, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=-3, reverse=True, as_business_day=True), self.time.next_day(offset=3, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=-11, reverse=True, as_business_day=True), self.time.next_day(offset=11, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=-27, reverse=True, as_business_day=True), self.time.next_day(offset=27, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=1, reverse=True, as_business_day=True), self.time.next_day(offset=-1, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=2, reverse=True, as_business_day=True), self.time.next_day(offset=-2, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=3, reverse=True, as_business_day=True), self.time.next_day(offset=-3, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=11, reverse=True, as_business_day=True), self.time.next_day(offset=-11, as_business_day=True))
        self.assertEqual(self.time.next_day(offset=27, reverse=True, as_business_day=True), self.time.next_day(offset=-27, as_business_day=True))
    
    def test_next_weekday(self):
        self.assertEqual(self.time.next_weekday(),   self.time.today() - 2 * self.day_offset)
        self.assertEqual(self.time.next_weekday(-1), self.time.today() - 2 * self.day_offset)
        self.assertEqual(self.time.next_weekday(-2), self.time.today() - 2 * self.day_offset)
        self.assertEqual(self.time.next_weekday(-3), self.time.today() - 3 * self.day_offset)
        self.assertEqual(self.time.next_weekday(-7), self.time.today() - 9 * self.day_offset)
        self.assertEqual(self.time.next_weekday(-8), self.time.today() - 9 * self.day_offset)
        self.assertEqual(self.time.next_weekday(-9), self.time.today() - 9 * self.day_offset)
        self.assertEqual(self.time.next_weekday(1),  self.time.today() + 1 * self.day_offset)

    def test_read_dates(self):
        self.assertEqual(self.time.read_dates(('2024-07-01', self.time.reference_date())), (date(2024, 7, 1), self.time.reference_date(as_type=date)))
        self.assertEqual(self.time.read_dates((self.time.reference_date(), '2024-07-01')), (self.time.reference_date(as_type=date), date(2024, 7, 1)))

if __name__ == '__main__':
    unittest.main()