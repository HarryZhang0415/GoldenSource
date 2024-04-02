import unittest
import time
import datetime

import pytz

from GoldenSource.python.common.services import NullLoggerService
from GoldenSource.python.db.database_service import DatabaseService
from GoldenSource.python.common.domain import Domain
from GoldenSource.python.time import now

# @unittest.skip("In Progress....")
class Test(unittest.TestCase):
    def setUp(self) -> None:
        domain = Domain()
        self.idle_timeout = 10
        domain.configuration._config[DatabaseService.__name__].setdefault('idle_timeout', self.idle_timeout)
        self.db_service = domain.get_service(DatabaseService)
        self.sybase = 'fundamentals'
        self.dbserver = 'fundamentals'

    def _some_sql_action(self, db):
        tbl = (
            "CREATE TEMPORARY TABLE UNITTEST"
            "("
            "INT_VAL int PRIMARY KEY"
            ", DATE_VAL datetime"
            ");"
        )
        db.execute(tbl)

        insert = "insert into UNITTEST values(%s, %s)"
        tz = pytz.UTC
        dt = now(timezone=tz)

        data = [(x, dt.replace(day=x, microsecond=0)) for x in range(1, 10)]

        db.executemany(insert, data)
        slct = "select INT_VAL, DATE_VAL from UNITTEST order by INT_VAL asc"
        response = db.executef(slct)
        for idx, record in enumerate(response):
            self.assertEqual(record, data[idx])

    def test_init(self):
        db1 = self.db_service[self.sybase]
        db2 = self.db_service.get(self.sybase)
        self.assertEqual(db1, db2)
        if db1.link_status:
            db1.close()
        if db2.link_status:
            db2.close()

    def test_overrides(self):
        db = self.db_service.get(user_id='harryzhang', password='Zh970415~', dbname=self.sybase)
        self.assertIsNotNone(db)
        if db.link_status:
            db.close()
    
    def test_non_cached_connection(self):
        db = self.db_service.new_connection(user_id='harryzhang', password='Zh970415~', dbname=self.sybase)
        self.assertIsNotNone(db)
        self._some_sql_action(db)
        if db.link_status:
            db.close()
    
    def test_shortcuts(self):
        sql = "select * from fundamentals.balance_sheet order by ID asc limit 10"

        try:
            for row in self.db_service.execute(self.dbserver, sql):
                pass
        except:
            with self.db_service.get(self.dbserver) as db:
                for row in db.executef(sql):
                    self.assertIsNotNone(row)
                    self.assertGreater(len(row), 0)
            
        for row in self.db_service.executef(self.dbserver, sql):
            self.assertIsNotNone(row)
            self.assertGreater(len(row), 0)

        for row in self.db_service.executefm(self.dbserver, sql):
            self.assertIsNotNone(row)
            self.assertGreater(len(row), 0)


    def test_simple_queries(self):
        db = self.db_service[self.sybase]
        self._some_sql_action(db)
        db.close()
        self.assertFalse(db.link_status)

    def test_contextual_use(self):
        db = self.db_service.get(self.dbserver)
        with db:
            self.assertTrue(db.link_status)
            self._some_sql_action(db)
        self.assertFalse(db.link_status)

    def test_autoreconnect(self):
        db = self.db_service.get(self.dbserver)
        with db:
            self.assertTrue(db.link_status)
            self._some_sql_action(db)
        self.assertFalse(db.link_status)

        self._some_sql_action(db)

        self.assertTrue(db.link_status)
        db.close()
        self.assertFalse(db.link_status)

    def test_timeout(self):
        db = self.db_service[self.dbserver]
        if self.db_service.is_recycle_running:
            time.sleep(self.idle_timeout * 2)
            self.assertFalse(db.link_status)
        else:
            self.assertTrue(db.link_status)
            db.close()
            self.assertFalse(db.link_status)

    def test_no_timeout_if_running(self):
        db = self.db_service[self.dbserver]
        if self.db_service.is_recycle_running:
            db.execute("DO SLEEP({})".format(self.idle_timeout * 2))
            self.assertTrue(db.link_status)
        else:
            self.assertTrue(db.link_status)
            db.close()
            self.assertFalse(db.link_status)
        db.close()
        self.assertFalse(db.link_status)

if __name__ == '__main__':
    unittest.main()