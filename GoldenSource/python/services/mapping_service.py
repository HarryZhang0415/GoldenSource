from collections import defaultdict

from GoldenSource.python.common.services import Service
from GoldenSource.python.common.mappings import BaseMappings, DatabaseMapping

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
        