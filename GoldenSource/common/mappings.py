from collections import defaultdict
from GoldenSource.common.services import Service
from GoldenSource.db.database_service import DatabaseService


class BaseMappings(object):
    def __init__(self) -> None:
        pass

    def getGroup(self, groupName):
        raise NotImplementedError('{}.getGroup'.format(self.__class__.__name__))
    
    def load(self, domain):
        raise NotImplementedError('{}.load'.format(self.__class__.__name__))
    
    def reload(self):
        raise NotImplementedError('{}.reload'.format(self.__class__.__name__))
    
    def lookupString(self, groupName, defaultVal, *args):
        raise NotImplementedError('{}.lookupString'.format(self.__class__.__name__))
    
    def lookupInt(self, groupName, defaultVal, *args):
        raise NotImplementedError('{}.lookupInt'.format(self.__class__.__name__))
    
    def lookupDouble(self, groupName, defaultVal, *args):
        raise NotImplementedError('{}.lookupDouble'.format(self.__class__.__name__))
    
    def lookupBool(self, groupName, defaultVal, *args):
        raise NotImplementedError('{}.lookupBool'.format(self.__class__.__name__))
    
    def insertMapping(self, groupName, value, *args):
        raise NotImplementedError('{}.insertMapping'.format(self.__class__.__name__))
    
    def deleteMapping(self, groupName, value, *args):
        raise NotImplementedError('{}.deleteMapping'.format(self.__class__.__name__))
    

class BaseMappingGroup(object):
    def __init__(self) -> None:
        pass

    def lookupString(self, groupName, defaultVal, *args):
        raise NotImplementedError('{}.lookupString'.format(self.__class__.__name__))
    
    def lookupInt(self, groupName, defaultVal, *args):
        raise NotImplementedError('{}.lookupInt'.format(self.__class__.__name__))
    
    def lookupDouble(self, groupName, defaultVal, *args):
        raise NotImplementedError('{}.lookupDouble'.format(self.__class__.__name__))
    
    def lookupBool(self, groupName, defaultVal, *args):
        raise NotImplementedError('{}.lookupBool'.format(self.__class__.__name__))
        

class BaseMappingUpdateListener(object):
    def onMappingsUpdate(self):
        pass


class mappingTemplate(object):
    def __init__(self, name, fields) -> None:
        self.categoryName = name
        self.nExpKeys = len(fields)
        self.header = ",".join(fields)

class MappingCategory(BaseMappingGroup):
    def __init__(self, template) -> None:
        self.template = template
        self.rawData = []
        self.mappings = Field()
        self.logger = None

    def add(self, keys, value):
        l = len(keys)
        if l < self.template.nExpKeys:
            self.logger.error('Invalid number of keys for mapping: %s', keys)
            return
        l = self.template.nExpKeys
        fldmap = self.mappings
        strout = ""
        for i in range(0, l-1):
            k = keys[i]
            if k not in fldmap:
                self.logger.error('Invalid key: %s', k)
                return
            strout += fldmap[k] + ","
            newfld = fldmap.get(k)
            if newfld is None:
                newfld = Field()
                fldmap.add(k, newfld)
            fldmap = newfld
        val = Value(value)
        fldmap.add(keys[l-1], val)
        strout += keys[l-1]
        self.rawData.append((strout, value))
        if self.logger is not None:
            self.logger.info('{}|Added Mapping|{}|{} --> {}', self.app_name, self.template.nExpKeys, strout, value)
        
        def lookup(self, *args):
            l = len(args)
            if l != self.template.nExpKeys:
                self.logger.error('Invalid number of keys for mapping: %s', args)
                return None
            mapping = self.mappings
            for key in args:
                if mapping.isMapping():
                    fldmap = mapping
                    mapping = fldmap.lookup(key)
                else:
                    return None
            if mapping is None or mapping.isMapping():
                return None
            return Value(mapping)
        
        def getAllPairs(self):
            return self.rawData
        
        def lookupString(self, defaultVal, *args):
            val = self.lookup(*args)
            if val is None:
                return defaultVal
            return val.getValue()
        
        def lookupInt(self, defaultVal, *args):
            val = self.lookup(*args)
            if val is None:
                return defaultVal
            return int(val.getValue())
        
        def lookupDouble(self, defaultVal, *args):
            val = self.lookup(*args)
            if val is None:
                return defaultVal
            return float(val.getValue())
        
        def lookupBool(self, defaultVal, *args):
            val = self.lookup(*args)
            if val is None:
                return defaultVal
            return bool(val.getValue())

class BaseMapping(object):
    def isMapping(self):
        return False
    
class Field(BaseMapping):
    DEFAULT = "_ALL_"

    def __init__(self) -> None:
        self.mappings = {}

    def add(self, key, mapping):
        self.mappings[key] = mapping

    def get(self, key):
        return self.mappings.get(key, None)

    def isMapping(self):
        return True
    
    def lookup(self, key):
        val = self.mappings.get(key, None)
        if not val: return self.mappings.get(self.DEFAULT)
        else: return val
    
class Value(BaseMapping):
    def __init__(self, strval) -> None:
        self.value = strval

    def isMapping(self):
        return False
    
    def getValue(self):
        return self.value
    
class DatabaseMapping(BaseMappings):
    def __init__(self, app_name):
        super(DatabaseMapping, self).__init__()
        self.app_name = app_name
        self.mappings = None
        self.templates = {}
        self.domain = None
        self.logger = None
    
    def getGroup(self, groupName):
        if self.mappings is None:
            return None
        cat = self.mappings.get(groupName, None)
        return cat

    def load(self, domain):
        self.domain = domain
        self.logger = domain.logger_service.get_logger(self.__class__.__name__)
        self.dbname = domain.get_param('DatabaseMapping', 'database')
        
        dbsvc = domain.get_service(DatabaseService)

        sql = """ select CATEGORY, FIELD1, FIELD2, FIELD3, FIELD4, FIELD5 from Ref_MAPPING_TYPES where NAME = {}""".format(self.app_name)
        rows = dbsvc.executef(self.dbname, sql)

        maps = []
        i=0
        for r in rows:
            strcategory = r[i]
            flds = []
            for f in range(1, 6):
                fld = r[i+f]
                fld = fld.strip()
                if len(fld) == 0: break
                flds.append(fld)
            maps.append((strcategory, flds))
        for pair in maps:
            category = mappingTemplate(pair[0], pair[1])
            self.templates[pair[0]] = category
            if self.logger is not None:
                self.logger.info('{}|Added Group:{}'.format(self.app_name, pair[0]))
        
        self.loadMappings(dbsvc)

    def reload(self):
        if self.domain is None:
            raise Exception("Cannot acquire database service with uninitialized domain")
        dbsvc = self.domain.get_service(DatabaseService)
        self.loadMappings(dbsvc)

    def loadMappings(self, dbsvc):
        sql = """ select CATEGORY, FIELD1, FIELD2, FIELD3, FIELD4, FIELD5, VALUE from GS_MAPPINGS where NAME = {}""".format(self.app_name)
        rows = dbsvc.executef(self.dbname, sql)
        maps = []
        i=0
        for r in rows:
            strcategory = r[i]
            flds = []
            for f in range(1, 6):
                fld = r[f]
                fld = fld.strip()
                flds.append(fld)
            strval = r[f+1]
            maps.append((strcategory, flds, strval))
        mappings = {}
        for t in maps:
            if t[2] == "_DELETED_":
                continue
            template = self.templates.get(t[0], None)
            if template == None: continue

            category = mappings.get(t[0], None)
            if category is None:
                category = MappingCategory(template)
                mappings[template.categoryName] = category
            category.add(t[1], t[2])
        
        self.mappings = mappings

    def lookupString(self, groupName, defaultVal, *args):
        cat = self.mappings.get(groupName, None)
        if cat is None:
            return defaultVal
        return cat.lookupString(defaultVal, *args)
    
    def lookupInt(self, groupName, defaultVal, *args):
        cat = self.mappings.get(groupName, None)
        if cat is None:
            return defaultVal
        return cat.lookupInt(defaultVal, *args)
    
    def lookupDouble(self, groupName, defaultVal, *args):
        cat = self.mappings.get(groupName, None)
        if cat is None:
            return defaultVal
        return cat.lookupDouble(defaultVal, *args)
    
    def lookupBool(self, groupName, defaultVal, *args):
        cat = self.mappings.get(groupName, None)
        if cat is None:
            return defaultVal
        return cat.lookupBool(defaultVal, *args)
    
    def deleteMapping(self, groupName, *args):
        self.insertMapping(groupName, "_DELETED_", *args)


class MappingService(Service):

    PROPERTY_PREFIX = 'MappingService'

    def __init__(self, domain) -> None:
        super().__init__(domain)
        self.domain = domain
        self.logger_service = domain.logger_service
        self.logger = self.logger_service.get_logger(self.__class__.__name__)
        self.mappings = defaultdict(BaseMappings)
        self.listeners = []
        self._load()

    def _load(self):
        app_names = self.domain.get_param(self.PROPERTY_PREFIX, 'database', default=None)
        if app_names is not None:
            sql = app_names.split(',')
            for app_name in sql:
                app_name = app_name.strip()
                m = self.mappings.get(app_name, None)
                if m is not None:
                    raise Exception("Found Conflicting Mapping<{}>".format(app_name))
                dbmap = DatabaseMapping(app_name)
                dbmap.load(self.domain)
                self.mappings[app_name] = dbmap
                self.logger.info('Loaded Mapping:{}'.format(app_name))

    def getMapping(self, strId):
        m = self.mappings.get(strId, None)
        if m is None:
            dbmap = DatabaseMapping(strId)
            try:
                dbmap.load(self.domain)
            except Exception as e:
                self.logger.error('Failed to load mapping {} : {}'.format(strId, e))
                return None
            self.mappings[strId] = dbmap
            m = dbmap
            self.logger.info("Loaded Database Mapping|{}".format(strId))
        return m
    
    def addListener(self, listener):
        if not listener in self.listeners:
            self.listeners.append(listener)

    def removeListener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def notifyListeners(self):
        for l in self.listeners:
            try:
                l.onMappingsUpdate()
            except:
                self.logger.error('Error notifying listener:{}'.format(l))

    def reload(self):
        self.logger.info('Reloading mappings...')
        for key in self.mappings.keys():
            m = self.mappings[key]
            try:
                self.logger.info('Reloading mapping:{}'.format(key))
                m.reload()
                self.logger.info('Mapping reloaded:{}'.format(key))
            except Exception as e:
                self.logger.error('Error reloading mapping:{}:{}'.format(key, e))
        
        self.notifyListeners()
        self.logger.info('Notified all listeners of the mapping update')
        