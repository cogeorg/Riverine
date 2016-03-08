import ast
import pandas
import random

import networkx as nx
from flask import render_template
from random import choice

from ModelVisualizer import ModelVisualizer


class RingVisualizer(ModelVisualizer):
    def __init__(self, _conf_obj):
        self.config_obj = _conf_obj

    def __del__(self):
        del self.config_obj

    def read_model_data(self):
        f = self.config_obj['model']['data']['file']['@value']
        try:
            file_data = pandas.read_csv(f, quotechar="'",
                skipinitialspace=True)
        except IOError:
            print 'Unable to open data model file', f
            return False
        # Get column headings from the xml config file
        self._parameters = self.config_obj['model']['data']['parameters']['param']
        self.param_keys = [self._parameters[i]['@id'] for i in range(len(self._parameters))]
        tmp = self.config_obj['model']['data']['column_names']['@value']
        column_headings = ast.literal_eval(tmp)
        # Here we don't need categories in the xml config file
        numParams = len(self.param_keys)
        if len(file_data.loc[0,:]) != numParams:
            print 'Column headings and parameters in config file inconsistent'
            return False
        column_index = range(0, numParams)
        if column_headings:
            row_index = range(1, len(file_data))
        else:
            row_index = range(0, len(file_data))
        self.modelData = {'nodes': [], 'edges': []}
        # Load node_data from xml configuration file
        node_data = self.config_obj['model']['data']['node_config']['node']
        if len(node_data) == 0:
            print 'No node data found in configuration file'
            return False
        # Load node_data from the xml configuration file
        # (assume structure of first key to be default)
        _node_keys = node_data[0].keys()
        self.node_keys = [key.encode('utf-8').translate(None, '@')
            for key in _node_keys]
        for node in node_data:
            tmp = {}
            for i in range(len(self.node_keys)):
                value = node[_node_keys[i]]
                if self.is_number(value):
                    value = ast.literal_eval(value)
                tmp.update({self.node_keys[i]: value})
            self.modelData['nodes'].append(tmp)
        # Load connection data from the csv data file
        for row in row_index:
            tmp = {};
            for col in column_index:
                value = file_data.iloc[row, col]
                tmp.update({self.param_keys[col]: value})
            self.modelData['edges'].append(tmp)
        if len(self.modelData['edges']) == 0:
            print 'No edge data found in configuration file'
            return False
        # for ring representation, no positions are needed
        return True

    def render_plot(self):
        # choose a random node as starting node
        focus = choice(self.modelData['nodes'])['node_id']
        self.js = render_template('dynamic_js/ring.js',
            conf_obj=self.config_obj, modelData=self.modelData, focus=focus)
        self.plot = render_template('ModelVisualizer/ring.html',
            js=self.js, modelData=self.modelData)
        return True

    def debug_mode(self, param):
        G = nx.gnm_random_graph(param['nNodes'], param['nEdges'])
        self.modelData = {'nodes': [], 'edges': []}
        # Store nodes in self.modelData['nodes']
        node_data = [n for n in G.nodes_iter()]
        for n in node_data:
            tmp = {'node_id': str(n), 'label': str(n),
                   'size': random.uniform(param['minNodeSize'],
                           param['maxNodeSize'])}
            self.modelData['nodes'].append(tmp)
        # Store category information
        edgeTypes = param['edgeTypes']
        num_edgeTypes = len(edgeTypes)
        edge_data = list(G.edges_iter(data=False))
        for e in edge_data:
            tmp = {'source': str(e[0]), 'target': str(e[1]), 
                   'strength': random.uniform(param['minEdgeStrength'],
                               param['maxEdgeStrength'])}
            self.modelData['edges'].append(tmp)
        return True
