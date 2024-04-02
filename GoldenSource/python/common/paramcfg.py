from copy import deepcopy
from GoldenSource.python.common.config import execfile

def showdict(x):
    for k in sorted(x.keys()):
        print(k, x[k])

class ParameterConfig(object):

    def __init__(self, dic=None, fromfile=None, delim=",") -> None:
        """
        Simple config container
        fromfile 
        """
        if fromfile is not None:
            fromfile = fromfile.split(":")
            dic = {}
            execfile(fromfile[0], dic)

            # only keep relevant keys
            dic = {k:v for k,v in dic.items() if k in fromfile[1].split(delim)}

        if dic is not None and len(dic) == 1:
            dic = dic.values()[0]
        self._dic = dic

    def __getitem__(self, key):
        return self._dic.get(key)
    
    def __setitem__(self, key, value):
        self._dic[key] = value

    def get(self, key, default=None):
        return self._dic.get(key, default)
    
    def as_dict(self, copy=False):
        return self._dic.copy() if copy else self._dic
    
    def keys(self):
        return self._dic.keys()
    
    def values(self):
        return self._dic.values()
    
    def items(self):
        return self._dic.items()
    
    def iterkeys(self):
        return self._dic.iterkeys()
    
    def itervalues(self):
        return self._dic.itervalues()
    
    def iteritems(self):
        return self._dic.items()
    
    def deepcopy(self):
        return self.__class__(dic=deepcopy(self._dic))
    
    def show(self, key=None):
        if key is None:
            showdict(self._dic)
        else:
            print(key, self._dic.get(key))

    def update(self, other, copy=False):
        if isinstance(other, ParameterConfig):
            other = other.as_dict()
        self._dic.update(other)
        
    