import os
from bisect import bisect_left, bisect_right
import datetime

# Nested dictionary
# n = ndict()
# n['k1']['k2'] = 1

def get_safe(dictionary, key, defvalue):
    value = dictionary.get(key, defvalue)
    return value if value else defvalue

def get_safe_object(object, key, defvalue):
    try:
        return object.__getattribute__(key)
    except:
        return defvalue
    
class ndict(dict):
    """
    Multi-level (nested) dictionary. Automatically adds new levels
    """

    def __missing__(self, key):
        self[key] = ndict()
        return self[key]
    
    def extract(self, extracted=None):
        """
        Extracts the leaf (deepest) level of the multi-level dictionary. Will NOT recurse into standard dictionaries.
        To recurse into standard dictionaries, see ndict.fast_extract.
        :returns A List containing the items at the leaves
        """
        if extracted is None:
            return []
        for k, v in self.items():
            if isinstance(v, ndict):
                v.extract(extracted)
            else:
                extracted.append(v)
        return extracted
    
    @staticmethod
    def extract_all(d, extracted=None):
        """
        Extracts the leaf (deepest) level of the multi-level dictionary. WILL recurse into standard dictionaries.
        To recurse only into ndicts, see extract.
        :param extracted: A list to store the results
        :return A list containing the items at the leaves
        """
        if extracted is None:
            return []
        for k, v in d.items():
            if isinstance(v, dict):
                ndict.extract_all(v, extracted)
            else:
                extracted.append(v)
        return extracted
    
    def flatten(self, flattened=None, parent_key='', sep="_"):
        """
        Flattens the nested dictionary into a single-level dictionary. The keys for flattened dictionary are the 
        concatenated keys for each level in ndict: d[1][2][3] -> d[1_2_3]. Will NOT recurse into standard dictionaries.
        To recurse into standard dictionaries, see ndict.fast_flatten.
        : param parent_key: Parent key to prepend to the flattened key
        : param sep: Separatar string to place between key levels
        : returns A flattened, single-level dictionary
        """
        if flattened is None:
            return {}
        for k, v in self.items():
            new_key = parent_key + sep + str(k) if parent_key else str(k)
            if isinstance(v, ndict):
                v.flatten(flattened=flattened, parent_key=new_key, sep=sep)
            else:
                flattened[new_key] = v
        return flattened
    
    @staticmethod
    def flatten_all(d, flattened=None, parent_key='', sep='_'):
        """
        Flattens the nested dictionary into a single-level dictionary. The keys for flattened dictionary are the 
        concatenated keys for each level in ndict: d[1][2][3] -> d[1_2_3]. WILL recurse into standard dictionaries.
        To recurse into only ndicts, see flatten.
        : param flattened: A dictionary to store the results
        : param parent_key: Parent key to prepend to the flattened key
        : param sep: Separator string to place between key levels
        : returns a flattened, single-level dictionary
        """
        if flattened is None:
            return {}
        for k, v in d.items():
            new_key = parent_key + sep + str(k) if parent_key else str(k)
            if isinstance(v, dict):
                ndict.flatten_all(v, flattened=flattened, parent_key=new_key, sep=sep)
            else:
                flattened[new_key] = v
        return flattened

def unique(lst):
    return list(set(lst))

def getFilesInDir(mypath=os.getcwd()):
    f = []
    dirpath = ''
    for (dirpath, dirnames, fielnames) in os.walk(mypath):
        f.extend(fielnames)
        break
    return f, dirpath

def find_range(array, a, b):
    start = bisect_right(array, a)
    end = bisect_left(array, b)
    return (start, end)

def chunks(l, n):
    """
    Yield successive n-sized chunks from l
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

class Iterable():
    def __init__(self) -> None:
        self.data = ndict()

    def __iter__(self):
        return self.data.__iter__()
    
    def __len__(self):
        return len(self.data)
    
    def __contains__(self, v):
        return v in self.data
    
    def __getitem__(self, v):
        return self.data[v]
    
    def __setitem__(self, k, v):
        self.data[k] = v

    def keys(self):
        return self.data.keys()
    
    def items(self):
        return self.data.items()
    
class iterableList():
    def __init__(self):
        self.data = []

    def __iter__(self):
        return self.data.__iter__()
    
    def __len__(self):
        return len(self.data)
    
    def __contains__(self, v):
        return v in self.data

    def __getitem__(self, v):
        return self.data[v]
    
    def __setitem__(self, k, v):
        self.data[k] = v

    def index(self, v):
        return self.data.index(v)

if __name__ == "__main__":

    a = [1, 2, 4, 6, 7, 8, 11]
    r = find_range(a, 4, 8)
    print(a[r[0]:r[1]])

    print(getFilesInDir())

    n = ndict()
    n['k1']['k3'] = 1
    n['k2']['k3'] = 2
    n['k3']['k4']['k5'] = 3
    print(n['k3']['k4']['k5'])