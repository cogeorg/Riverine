import ast
import json
import numpy as np
from difflib import SequenceMatcher

from flask import render_template

from ModelVisualizer import ModelVisualizer


class GeomapVisualizer(ModelVisualizer):
    def __init__(self, _conf_obj):
        self.config_obj = _conf_obj;
        self.country_compilation = None
        self.country_coordinates = None
        try:
            with open('static/json/country_compilation.min.json', 'r') as fp:
                self.country_compilation = json.load(fp)
        except IOError:
            print 'Cannot open static/json/country_compilation.min.json'
        try:
            with open('static/json/countries.json', 'r') as fp:
                self.country_coordinates = json.load(fp)
        except IOError:
            print 'Cannot open static/json/country_compilation.min.json'

    def __del__(self):
        del self.config_obj
        del self.country_compilation

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def getCode(self, query_country):
        if self.country_compilation is None:
            return None
        code = None
        bestscore = .7;
        for i in range(len(self.country_compilation)):
            probe_country = self.country_compilation[i]['country']
            probe_country_alias = self.country_compilation[i]['country_alias']
            score = self.similar(probe_country.lower(), query_country.lower())
            if probe_country_alias is not None:
                score_alias = self.similar(probe_country_alias.lower(),
                    query_country.lower())
                score = max(score, score_alias)
            if (score > bestscore):
                bestscore = score
                code = self.country_compilation[i]['id']
        return code

    def read_model_data(self):
        f = self.config_obj['model']['data']['file']['@value']
        try:
            file_data = np.genfromtxt(f, delimiter=',', dtype=None)
        except IOError:
            print 'Unable to open data model file', f
            return False
        # Get column headings from xml config file
        self._parameters = self.config_obj['model']['data']['parameters']['param']
        self.param_keys = []
        for i in range(len(self._parameters)):
            self.param_keys.append(self._parameters[i]['@id'])
        tmp = self.config_obj['model']['data']['column_names']['@value']
        column_headings = ast.literal_eval(tmp)
        # Get categories from xml config file
        self._categories = self.config_obj['model']['data']['categories']['category']
        self.categories_keys = []
        self.categories_labels = []
        n = len(self._categories)
        for i in range(n):
            self.categories_keys.append(self._categories[i]['@value'])
            self.categories_labels.append(self._categories[i]['@label'])
        numParams = len(self.param_keys)
        if len(file_data[0]) != numParams:
            print 'Column headings and parameters in config file inconsistent.'
            return False
        column_index = range(0, numParams)
        if column_headings:
            row_index = range(1, len(file_data))
        else:
            row_index = range(0, len(file_data))
        # Load data from file_data into a dictionary
        self.modelData = []
        for row in row_index:
            tmp = {};
            for col in column_index:
                value = file_data[row][col]
                if self.is_number(value):
                    value = ast.literal_eval(value)
                # read the data from the file
                tmp.update({self.param_keys[col]:value})   
            # map the country to a geomap code; skip the row if no code found
            code = self.getCode(tmp['country'])
            if code is not None:    
                tmp.update({'code': code})
                self.modelData.append(tmp)
        if len(self.modelData) == 0:
            return False
        return True

    def render_plot(self):
        categories = []
        for i in range(len(self.categories_keys)):
            _range = self.find_min_max(self.modelData,self.categories_keys[i])
            categories.append(({'value': i, 'key': self.categories_keys[i],
                                'label': self.categories_labels[i],
                                'min': _range[0], 'max': _range[1]}))
        self.js = render_template('dynamic_js/geomap.js',
            conf_obj=self.config_obj, categories=categories,
            modelData=self.modelData, coords=self.country_coordinates)
        self.plot = render_template('ModelVisualizer/geomap.html',
            js=self.js, categories=categories)
        return True
