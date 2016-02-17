# -*- coding: utf-8 -*-

from flask import render_template
import xmltodict
import numpy as np
import ast
import json
from difflib import SequenceMatcher
import sys
import pdb
import pandas


# We use the Template Method design pattern to define the ModelVisualizer class
class ModelVisualizer(object):
    # define member variables
    # define member functions
    def __init__(self): 
        # class constructor
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
        _min,_max = sys.maxint,-sys.maxint-1
        for x in (item[key] for item in dict_list):
            _min,_max = min(x,_min),max(x,_max)
        return [_min,_max]

    def read_config_file(self, file):
        try:           
            self.config_obj = xmltodict.parse(file)
        except IOError:
            print 'Unable to parse file.', file
            return False
        return True
