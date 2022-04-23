import requests
import tarfile
import io

class ReadRepoDB:
    def __init__(self, db_path):
        self.__db_path = db_path
        self.__db = list()
    
    def __parse_desc(self, desc_):
        desc = desc_.read().decode('utf-8')
        lines = [i.strip() for i in desc.split('\n') if i.strip()]
        lines.append('%DNE%')
        
        k, d, l = None, dict(), list()
        for i in lines:
            if i.startswith('%') and i.endswith('%'):
                if l:
                    d[k] = l[0] if len(l) == 1 else l
                l = list()
                k = i.strip('%').lower()
                continue
            l.append(i)
        self.__db.append(d)
    
    def __fmt_dict(self):
        d = dict()
        for i in self.__db:
            k = i.pop('name')
            d[k] = i
        return d
    
    def __read_impl(self, f):
        with tarfile.open(fileobj=f, mode='r') as f:
            for member in f.getmembers():
                desc = f.extractfile(member)
                if desc:
                    self.__parse_desc(desc)
                    desc.close()

    def __read_resolv_path(self):
        path_low = self.__db_path.lower()
        if path_low.startswith('http://') or path_low.startswith('https://'):
            f = io.BytesIO(requests.get(self.__db_path).content)
            self.__read_impl(f)
            return
        with open(self.__db_path, 'rb') as f:
            self.__read_impl(f)
            
    def read(self, dict_format=True):
        try:
            self.__read_resolv_path()
        except:
            pass        
        if dict_format:
            return self.__fmt_dict()
        return self.__db
