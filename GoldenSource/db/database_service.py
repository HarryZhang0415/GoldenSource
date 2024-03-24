from threading import RLock, current_thread, Event
import datetime

import pandas
from mysql.connector import MySQLConnection, Error as ConnectionError, ProgrammingError, errorcode
from GoldenSource.utils.data_types import ndict
from GoldenSource.common.concurrency import Timer
from GoldenSource.common.domain import Domain
from GoldenSource.common.services import Service
from GoldenSource.utils.patterns import Singleton

class DatabaseConnection(object):

    def __init__(self, host, user_id, password, dbname, **kwargs):
        domain = Domain()
        self.logger = domain.logger_service.get_logger(self.__class__.__name__)

        self.host = host
        self.user_id = user_id
        self.password = password
        self.dbname = dbname
        self.fast_execute = domain.get_param('database', 'fast_execute', default = False)
        self.extra_args = kwargs

        # Set app name on db connection
        app = domain.get_param('app', 'full_name')
        if not app:
            path = domain.get_param('app', 'config_path')
            app = domain.get_param('app', 'config_file')[len(path) + 1:]
        if not app:
            import sys
            import os
            if sys.argv and sys.argv[0]:
                app = os.path.basename(sys.argv[0])
        if not app:
            app = 'python DatabaseConnection'

        self.connection_confg = {
            'host': self.host,
            'user': self.user_id,
            'password': self.password,
            'database': self.dbname
        }

        if "port" not in self.extra_args:
            self.connection_confg["port"] = 3306

        if "autocommit" not in self.extra_args:
            self.connection_confg["autocommit"] = True

        self._queried = False
        self._entered = False
        self._last_use_time = datetime.datetime.now()
        self.conn = None
        self.cursor = None
        self.connect()

    @property
    def link(self):
        """
        :return The underlying link
        """
        return self.conn
    
    @property
    def link_status(self):
        """
        :return True if the link is up
        """
        return self.cursor is not None
    
    @property
    def is_in_use(self):
        return self._queried or self._entered
    
    @property
    def last_use_time(self):
        if self.is_in_use:
            return datetime.datetime.now()
        return self._last_use_time
    
    def __enter__(self):
        self._entered = True
        if not self.link_status:
            self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        self._entered = False
        return exc_type is None
    
    def connect(self):
        """
        Connect to the database
        """
        try:
            self.conn = MySQLConnection(**self.connection_confg)
            self.cursor = self.conn.cursor()
            if self.fast_execute:
                self.cursor.fast_executemany = True
            self.logger.debug("Connected to database: %s", self)
        except ConnectionError as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.logger.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.logger.error("Database does not exist")
            else:
                self.logger.error(err)
            raise
        except Exception as e:
            self.logger.exception("Failed to connect to database: %s due to %s".format(self.connection_confg['database'], e))
            raise

    def close(self):
        if not self.link_status:
            return
        try:
            self.cursor = None
            self.conn.close()
            self.logger.debug("Disconnected from {}".format(self))
        except:
            self.logger.exception("Failed to disconnect from database: %s", self)
        
    def _on_disconnect(self, reason = None):
        if self.link_status:
            self.logger.error("Disconnected from {}/{}: {}".format(self.host, self.dbname, reason))
            self.cursor = None
        self.connect()
    
    def __str__(self) -> str:
        return "{}<{}>".format(self.host, self.dbname)

    def __repr__(self) -> str:
        return "{}({!r},{!r},{!r},{!r},{})".format(self.__class__.__name__, self.user_id, self.password, self.host, self.dbname, \
                                                   ",".join("{}={!r}".format(k, v) for k, v in self.extra_args.items()))
    
    def list(self):
        pass

    def _cursor_execute(self, sql, *data):
        try:
            self._queried = True
            if not self.link_status:
                raise ConnectionError("Connection is not open")
            return self.cursor.execute(sql, *data)
        except ConnectionError as e:
            self._on_disconnect(e)
            return self.cursor.execute(sql, *data)
        finally:
            self._last_use_time = datetime.datetime.now()
            self._queried = False
    
    def _cursor_executemany(self, sql, data):
        assert (isinstance(data, list))
        try:
            self._queried = True
            if not self.link_status:
                raise ConnectionError("Connection is not open")
            return self.cursor.executemany(sql, data)
        except ConnectionError as e:
            self._on_disconnect(e)
            return self.cursor.executemany(sql, data)
        finally:
            self._last_use_time = datetime.datetime.now()
            self._queried = False

    def _cursor_as_dataframe(self, sql, data=None, index_col=None, coerce_float=True):
        try:
            self._queried = True
            if not self.link_status:
                raise ConnectionError("Connection is not open")
            return pandas.read_sql(sql, self.conn, index_col=index_col, coerce_float=coerce_float,params=data)
        except ConnectionError as e:
            self._on_disconnect(e)
            return pandas.read_sql(sql, self.conn, index_col=index_col, coerce_float=coerce_float,params=data)
        finally:
            self._last_use_time = datetime.datetime.now()
            self._queried = False
    
    def execute(self, sql, *data):
        return self._cursor_execute(sql, *data)
    
    def executef(self, sql, *data):
        self._cursor_execute(sql, *data)
        return self.cursor.fetchall()
    
    def executef_safe(self, sql, *data):
        try:
            self._cursor_execute(sql, *data)
            return self.cursor.fetchall()
        except ProgrammingError as e:
            self.logger.error("Error executing query: %s due to %s".format(sql, e))
            return []
            
    # Safe execute fetch and will return the first table result
    # tested with Sybase and MySql to deal with count issues/etc
    def executef_one(self, sql, retry=1, *data):
        descr = rows = None
        try:
            self._queried = True
            if not self.link_status:
                raise ConnectionError("Link down")
            cur_exec = self.cursor.execute(sql, *data)
            for cnt in range(1, 7): # Test results upt to 6 sets (as a safety not to run forever)
                if self.cursor.description:
                    descr = self.cursor.description
                    rows = self.cursor.fetchall()
                    break
                if not self.cursor.nextset():
                    break
            return descr, rows
        except ConnectionError as e:
            self._on_disconnect(e)
            return self.executef_one(sql, retry - 1, *data) if retry > 0 else (None, None)
        finally:
            self._last_use_time = datetime.datetime.now()
            self._queried = False
    
    def executefm(self, sql, *data):
        self._cursor_execute(sql, *data)
        return self.cursor.fetchmany()
    
    def executemany(self, sql, data):
        return self._cursor_executemany(sql, data)
    
    def read(self, sql, data=tuple(), row_mapper=None):
        if row_mapper is None:
            row_mapper = lambda row: row
        else:
            assert callable(row_mapper)
        return [row_mapper(row) for row in self._cursor_execute(sql, data)]
    
    def read_as_dataframe(self, sql, data=None, index_col=None, coerce_float=True):
        return self._cursor_as_dataframe(sql, data, index_col, coerce_float)
    
    def commit(self):
        try:
            self._queried = True
            if not self.link_status:
                raise ConnectionError("Connection is not open")
            self.cursor.commit()
        except ConnectionError as e:
            self._on_disconnect(e)
        finally:
            self._last_use_time = datetime.datetime.now()
            self._queried = False
    
    def simple_select(self, table_name, header_columns, data_columns, show_sql=False):
        new_header = []
        for idx, h in enumerate(header_columns):
            if type(h) == list:
                if len(h) == 2:
                    new_header.append(h[0] + " AS " + h[1])
                    header_columns[idx] = h[1]
                if len(h) == 3:
                    new_header.append(h[0] + " AS " + h[2])
                    header_columns[idx] = h[1]
            else:
                new_header.append(h)
        
        new_data = []

        for idx, h in enumerate(data_columns):
            if type(h) == list:
                if len(h) == 2:
                    new_data.append(h[0] + " AS " + h[1])
                    data_columns[idx] = h[1]
                if len(h) == 3:
                    new_data.append(h[0] + " AS " + h[2])
                    data_columns[idx] = h[1]
            else:
                new_data.append(h)
        
        sql = """
        SELECT %s
        FROM %s
        """ % (",".join(new_header + new_data), table_name)
        if show_sql:
            print(sql)
        
        return self.query2dict(sql, header_columns, data_columns)
    
    def query2dict(self, sql, header_columns, data_columns):
        ret = ndict()
        column_map = dict()
        for i, row in enumerate(self.executef(sql)):
            if i == 0:
                columns = [t[0] for t in row.cursor_description]
                for c in header_columns + data_columns:
                    column_map[c] = columns.index(c)
            
            data = dict()
            for c in data_columns:
                data[c] = row.__getattribute__(c)
            if len(header_columns) == 1:
                ret[row.__getattribute__(header_columns[0])] = data
            if len(header_columns) == 2:
                ret[row.__getattribute__(header_columns[0])][row.__getattribute__(header_columns[1])] = data
            if len(header_columns) == 3:
                ret[row.__getattribute__(header_columns[0])][row.__getattribute__(header_columns[1])][row.__getattribute__(header_columns[2])] = data
            if len(header_columns) == 4:
                ret[row.__getattribute__(header_columns[0])][row.__getattribute__(header_columns[1])][row.__getattribute__(header_columns[2])][row.__getattribute__(header_columns[3])] = data
            if len(header_columns) == 5:
                ret[row.__getattribute__(header_columns[0])][row.__getattribute__(header_columns[1])][row.__getattribute__(header_columns[2])][row.__getattribute__(header_columns[3])][row.__getattribute__(header_columns[4])] = data
        
        return ret
    
    def getCols(self):
        return [t[0] for t in self.cursor.cursor_description]
    
    def getColsFromRow(self, row):
        return [t[0] for t in row.cursor_description]
    
    def getHostname(self):
        return self.executef("SELECT @@SERVERNAME")
    

class DatabaseService(Service, metaclass=Singleton):

    def __init__(self, domain) -> None:
        super().__init__(domain)
        self._logger = domain.logger_service.get_logger(self.__class__.__name__)
        self._databases = domain.get_param('databases', default = {})
        self._connections = {}
        self._global_lock = RLock()
        self._locks = {}

        self._idle_timeout = domain.get_param(self.__class__.__name__, 'idle_timeout', as_type=int, default = 0)
        self._idle_timeout_event = Event()
        if self._idle_timeout > 0:
            self._idle_timer = Timer(event=self._idle_timeout_event, fcn=self._recycle, interval=int(self._idle_timeout / 2), name="Recycle")
            self._idle_timer.start()

    @property
    def is_recycle_running(self):
        return self._idle_timeout > 0
    
    def shutdown(self):
        self._idle_timeout_event.set()
        with self._global_lock:
            for db in self._connections.values():
                if db.link_status:
                    db.close()

    def _recycle(self):
        with self._global_lock:
            timeout = datetime.datetime.now() - datetime.timedelta(seconds=self._idle_timeout)
            for k, db in self._connections.items():
                thread_name = k[0].name
                self._logger.debug(
                    "Checking {}/{}: UP[{}] IN_USE[{}] LAST_USE[{}]".format(
                        thread_name,
                        db,
                        db.link_status,
                        db.is_in_use,
                        db.last_use_time.isoformat()
                    )
                )
                if db.link_status and not db.is_in_use and db.last_use_time <= timeout:
                    self._logger.info("Closing {}/{}, idle for over {} seconds".format(thread_name, db, self._idle_timeout))
                    db.close()
    
    @property
    def database_service_names(self):
        """
        Returns a list of the available aliases
        """
        return self._databases.keys()
    
    def __getitem__(self, dbname):
        """
        Returns the cached connection, creating it if required
        """
        return self.get(dbname)
    
    def get(self, dbname, **kwargs):
        """
        Returns the cached connection, creating it if required
        Extra arguments can be provided to override some or all of the builtin parameters of the connection:
        - uid: user id
        - pwd: password
        - dbname: the database name
        """
        thread_id = current_thread()
        key = (thread_id, dbname)
        if key not in self._connections:
            self._initiate_connection(thread_id, dbname, **kwargs)
        return self._connections[key]
    
    def _extract_param(self, param_name, kwargs, db_info):
        param_value = kwargs.get(param_name)
        if param_value:
            kwargs.pop(param_name)
            return param_value
        else:
            return db_info.get(param_name)
        
    def new_connection(self, dbname, **kwargs):
        """
        Create a new connection to the database
        """
        db_info = self._databases.get(dbname, {})
        if not db_info:
            raise ValueError("Database not found: {}".format(dbname))
        
        host = self._extract_param('host', kwargs, db_info)
        user_id = self._extract_param('user_id', kwargs, db_info)
        password = self._extract_param('password', kwargs, db_info)
        
        return DatabaseConnection(host, user_id, password, dbname, **kwargs)
    
    def execute(self, dbname, sql, *data):
        """
        This is a shortcut that can be called if and only if the result is not required. Because the underlying cursor is closed, iterating over the 
        results will be impossible. Use the with db: db.execute() construction if the results are required.
        Shortcut that calls
        >>> with db_service.get(dbname) as db:
            result = db.execute(sql, *data)
        
        The connection is closed on exiting the function
        """
        with self[dbname] as db:
            return db.execute(sql, *data)
        
    def executef(self, dbname, sql, *data):
        """
        Shortcut that calls
        >>> with db_service.get(dbname) as db:
            result = db.executef(sql, *data)
        
        The connection is closed on exiting the function
        """
        with self[dbname] as db:
            return db.executef(sql, *data)
        
    def executefm(self, dbname, sql, *data):
        """
        Shortcut that calls
        >>> with db_service.get(dbname) as db:
            result = db.executefm(sql, *data)
        
        The connection is closed on exiting the function
        """
        with self[dbname] as db:
            return db.executefm(sql, *data)

    def executemany(self, dbname, sql, data):
        """
        Shortcut that calls
        >>> with db_service.get(dbname) as db:
            result = db.executemany(sql, data)
        
        The connection is closed on exiting the function
        """
        with self[dbname] as db:
            return db.executemany(sql, data)
        
    def read(self, dbname, sql, data=tuple(), row_mapper=None):
        """
        Shortcut that calls
        >>> with db_service.get(dbname) as db:
            result = db.read(sql, data, row_mapper)
        
        The connection is closed on exiting the function
        """
        with self[dbname] as db:
            return db.read(sql, data, row_mapper)
        
    def read_as_dataframe(self, dbname, sql, data=None, index_col=None, coerce_float=True):
        """
        Shortcut that calls
        >>> with db_service.get(dbname) as db:
            result = db.read_as_dataframe(sql, data, index_col, coerce_float)
        
        The connection is closed on exiting the function
        """
        with self[dbname] as db:
            return db.read_as_dataframe(sql, data, index_col, coerce_float)
        
    def simple_select(self, dbname, table_name, header_columns, data_columns, show_sql=False):
        """
        Shortcut that calls
        >>> with db_service.get(dbname) as db:
            result = db.simple_select(table_name, header_columns, data_columns, show_sql)
        
        The connection is closed on exiting the function
        """
        with self[dbname] as db:
            return db.simple_select(table_name, header_columns, data_columns, show_sql)
        
    def query2dict(self, dbname, sql, header_columns, data_columns):
        """
        Shortcut that calls
        >>> with db_service.get(dbname) as db:
            result = db.query2dict(sql, header_columns, data_columns)
        
        The connection is closed on exiting the function
        """
        with self[dbname] as db:
            return db.query2dict(sql, header_columns, data_columns)
        
    def _initiate_connection(self, thread_id, dbname, **kwargs):
        
        key = (thread_id, dbname)
        db = self._connections.get(key)
        if db is None:
            with self._lock(thread_id):
                db = self._connections.get(key)
                if db is None:
                    db = self._connections.setdefault(key, self.new_connection(dbname, **kwargs))

        return db
    
    def _lock(self, thread_id=None):
        """
        Returns the thread-bound lock, effectively creating it if non-existing
        """
        if not thread_id:
            thread_id = current_thread()
        if thread_id not in self._locks:
            with self._global_lock:
                if thread_id not in self._locks:
                    self._locks[thread_id] = RLock()
        
        return self._locks[thread_id]