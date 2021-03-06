import ast
import numpy as np

from flask import render_template

from ModelVisualizer import ModelVisualizer


class BarplotVisualizer(ModelVisualizer):
    def __init__(self, _conf_obj):
        self.config_obj = _conf_obj

    def __del__(self):
        del self.config_obj

    def read_model_data(self):
        f = self.config_obj['model']['data']['file']['@value']
        try:
            file_data = np.genfromtxt(f, delimiter=',', dtype=None)
        except IOError:
            print 'Unable to open data model file', f
            return False
        # Get column headings from xml config file
        tmp = self.config_obj['model']['data']['column_names']['@value']
        column_headings = ast.literal_eval(tmp)
        column_index = range(1, len(file_data[0]))
        if column_headings:
            row_index = range(1, len(file_data))
        else:
            row_index = range(0, len(file_data))
        # Get the column headings from the xml config file
        self._parameters = self.config_obj['model']['data']['parameters']['param']
        self.param_keys = []
        for i in range(len(self._parameters)):
            self.param_keys.append(self._parameters[i]['@id'])
        # Get categories from xml config file
        self._categories = self.config_obj['model']['data']['categories']['category']
        self.categories_keys = []
        for i in range(len(self._categories)):
            self.categories_keys.append(self._categories[i]['@value'])
        # Load data from file_data into a dictionary
        self.modelData = []
        for row in row_index:
            for col in column_index:
                # first column is common to all other columns
                tmp = {self.param_keys[0]: ast.literal_eval(file_data[row][0])}
                # the next columns represent the data to be read in
                tmp.update({self.param_keys[1]:
                    ast.literal_eval(file_data[row][col])})
                # store the category
                tmp.update({self.param_keys[2]: self.categories_keys[col-1]})
                self.modelData.append(tmp)
        return True

    def render_plot(self):
        self.js = render_template('dynamic_js/barplot.js',
            conf_obj=self.config_obj, modelData=self.modelData)
        self.plot = render_template('ModelVisualizer/barplot.html',
            js=self.js,categories=sorted(list(self.categories_keys)))
        return True
