import sys
import xmltodict


# We use the Template Method design pattern to define the ModelVisualizer class
class ModelVisualizer(object):
    def __init__(self): 
        self.config_obj = None

    def __del__(self):
        del self.config_obj
        
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def find_min_max(self, dict_list, key):
        _min = sys.maxint
        _max = -sys.maxint - 1
        for x in (item[key] for item in dict_list):
            _min = min(x, _min)
            _max = max(x, _max)
        return [_min, _max]

    def read_config_file(self, f):
        try:           
            self.config_obj = xmltodict.parse(f)
        except IOError:
            print 'Unable to parse file', f
            return False
        return True
