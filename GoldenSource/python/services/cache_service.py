from GoldenSource.python.common.services import Service

class CacheService(Service):
    """
    Generic cache service
    """
    GETITEM_DEFAULT = object()

    def __init__(self, domain) -> None:
        super(CacheService, self).__init__(domain)
        self._cache = {}

    def _retrieve(self, item):
        raise NotImplementedError('{0.__class__.__name__} does not implement _retrieve'.format(self))
    
    def __getitem__(self, item):
        value = self._cache.get(item)
        if value is None:
            value = self._retrieve(item)
            if value is None:
                raise KeyError(item)
            self._cache[item] = value
        return value
    
    def get(self, item, default=None):
        value = self._cache.get(item)
        if value is None:
            value = self._retrieve(item)
            if value is None:
                value = default
            self._cache[item] = value
        return value