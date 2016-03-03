import ast
import pandas

from flask import render_template

from ModelVisualizer import ModelVisualizer


class HistogramVisualizer(ModelVisualizer):
    def __init__(self, _conf_obj):
        self.config_obj = _conf_obj

    def __del__(self):
        del self.config_obj

    def read_model_data(self):
        f = self.config_obj['model']['data']['file']['@value']
        try:
            file_data = pandas.read_csv(f,
                quotechar="'", skipinitialspace=True)
        except IOError:
            print 'Unable to open data model file', f
            return False
        # Get column headings from xml config file
        self._parameters = self.config_obj['model']['data']['parameters']['param']
        self.param_keys = [] # column headings of csv data file
        self.headers = [] # corresponding labels of the column headings (for visualization purposes)
        self.data_id = None # the column id which contains the data values 
        if len(file_data.columns) == 1:
            self.param_keys.append(self._parameters['@id'])
            self.headers.append(self._parameters['@label'])
            if self._parameters['@value'] == 'id':
                self.data_id = {'id': self._parameters['@id'], 'column': 0}
        else:
            for i in range(len(self._parameters)):
                self.param_keys.append(self._parameters[i]['@id'])
                self.headers.append(self._parameters[i]['@label'])
                if self._parameters[i]['@value'] == 'id':
                    self.data_id = {'id': self._parameters[i]['@id'], 'column': i}
        tmp = self.config_obj['model']['data']['column_names']['@value']
        column_headings = ast.literal_eval(tmp)
        # Get categories from xml config file
        self.categories = []
        self.categories_keys = []
        self.categories_labels = []
        for i in range(len(self.categories)):
            self.categories_keys.append(self.categories[i]['@value'])
            self.categories_labels.append(self.categories[i]['@label'])
        numParams = len(self.param_keys)
        if len(file_data.loc[0,:]) != numParams:
            print 'Column headings and parameters in config file inconsistent.'
            return False
        column_index = range(0, numParams)
        self.modelData = []
        # Load data from file_data into a list
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
        self.js = render_template('dynamic_js/histogram.js',
            conf_obj=self.config_obj, data_id=self.data_id,
            headers=self.headers, modelData=self.modelData)
        self.plot = render_template('ModelVisualizer/histogram.html',
            js=self.js, modelData=self.modelData)
        return True
