# -*- coding: utf-8 -*-

from ModelVisualizer import *
import pandas


class CandlestickVisualizer(ModelVisualizer):
    def __init__(self, _conf_obj):
        self.config_obj = _conf_obj

    def __del__(self):
        del self.config_obj

    def read_model_data(self):
        modelData_filename = self.config_obj['model']['data']['file']['@value']
        try:
            file_data = pandas.read_csv(modelData_filename, quotechar="'", skipinitialspace=True)
        except IOError:
            print 'Unable to open data model file:', modelData_filename
            return False
        #get the column headings from the xml config file
        self._parameters = self.config_obj['model']['data']['parameters']['param']
        self.param_keys = [] # column headings of csv data file
        self.headers = [] # corresponding labels of the column headings (for visualization purposes)
        self.data_id = None # the column id which contains the data values
        for i in range(len(self._parameters)):
            self.param_keys.append(self._parameters[i]['@id'])
            self.headers.append(self._parameters[i]['@label'])
            if self._parameters[i]['@value'] == 'id':
                self.data_id = {'id': self._parameters[i]['@id'], 'column': i}
        tmp = self.config_obj['model']['data']['column_names']['@value']
        column_headings = ast.literal_eval(tmp)
        # get the categories from the xml config file
        self.categories = []
        self.categories_keys = []
        self.categories_labels = []
        n = len(self.categories)
        for i in range(n):
            self.categories_keys.append(self.categories[i]['@value'])
            self.categories_labels.append(self.categories[i]['@label'])
        numParams = len(self.param_keys)
        if len(file_data.loc[0,:]) != numParams:
            print 'Column headings and parameters in the config file are inconsistent.'
            return False
        
        column_index = range(0,numParams)
        self.modelData = []
        #load the raw data from the csv data file
        for row in range(len(file_data)):
            tmp = []
            for col in column_index:
                value = file_data.loc[row,self.param_keys[col]]
                tmp.append(value)
            self.modelData.append(tmp)
        if len(self.modelData) == 0:
            return False
        return True

    def render_plot(self):
        self.js = render_template('dynamic_js/candlestick.js', conf_obj=self.config_obj, data_id = self.data_id,
                        headers=self.headers, modelData=self.modelData)
        self.plot = render_template('ModelVisualizer/candlestick.html', js = self.js,
                        modelData = self.modelData)
        return True
