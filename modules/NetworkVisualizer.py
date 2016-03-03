# -*- coding: utf-8 -*-
from ModelVisualizer import * 
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout # workaround for bug in nx 1.10
import random



class NetworkVisualizer(ModelVisualizer):
    def __init__(self, _conf_obj):
        self.config_obj = _conf_obj

    def __del__(self):
        del self.config_obj

    def read_model_data(self):
        modelData_filename = self.config_obj['model']['data']['file']['@value']
        try:
            file_data = np.genfromtxt(modelData_filename, delimiter=',', dtype=None)
        except IOError:
            print 'Unable to open data model file:', modelData_filename
            return False
        # get the column headings from the xml config file
        self._parameters = self.config_obj['model']['data']['parameters']['param']
        self.param_keys = [self._parameters[i]['@id'] for i in range(len(self._parameters))]
        tmp = self.config_obj['model']['data']['column_names']['@value']
        column_headings = ast.literal_eval(tmp)
        # get the categories from the xml config file
        self.categories = self.config_obj['model']['data']['categories']['category']
        self.categories_keys = [self.categories[i]['@value'] for i in range(len(self.categories))]
        self.categories_labels = [self.categories[i]['@label'] for i in range(len(self.categories))]
        numParams = len(self.param_keys)
        if len(file_data[0]) != numParams:
            print 'Column headings and parameters in config file inconsistent'
            return False
        column_index = range(0,numParams)
        if column_headings:
            row_index = range(1,len(file_data))
        else:
            row_index = range(0,len(file_data))
        self.modelData = {'nodes': [], 'edges': []}
        # load node_data from xml configuration file
        node_data = self.config_obj['model']['data']['node_config']['node']
        if len(node_data) == 0:
            print 'No node data found in configuration file'
            return False
        # take structure of first key as default
        _node_keys = node_data[0].keys()
        self.node_keys = [key.encode('utf-8').translate(None, '@') for key in _node_keys]
        for node in node_data:
            tmp = {}
            for i in range(len(self.node_keys)):
                value = node[_node_keys[i]]
                if self.is_number(value):
                    value = ast.literal_eval(value)
                tmp.update({self.node_keys[i]: value})
            self.modelData['nodes'].append(tmp)
        first_node = self.modelData['nodes'][0]
        # load connection_data from the csv data file
        for row in row_index:
            tmp = {};
            for col in column_index:
                value = file_data[row][col]
                if self.is_number(value):
                    value = ast.literal_eval(value)
                tmp.update({self.param_keys[col]:value})
            self.modelData['edges'].append(tmp)
        if len(self.modelData['edges']) == 0:
            print 'No edge data found in configuration file'
            return False
        # for large networks we should provide node positions
        # for small networks we can calculate them here or provide them
        # d3plus can also calculate them but positions will be random
        if not ('x' in first_node and 'y' in first_node):
            G = nx.Graph()
            edges = [(edge['source'], edge['target'], edge['strength'])
                     for edge in self.modelData['edges']]
            G.add_weighted_edges_from(edges)
            pos = graphviz_layout(G)
            for entry in self.modelData['nodes']:
                node = entry['node_id']
                entry['x'] = pos[node][0]
                entry['y'] = pos[node][1]
        return True

    def render_plot(self):
        self.js = render_template('dynamic_js/network.js', conf_obj=self.config_obj,
                        categories=self.categories, modelData=self.modelData)
        self.plot = render_template('ModelVisualizer/network.html', js=self.js, 
                        modelData=self.modelData, categories=self.categories)
        return True

    def debug_mode(self, param, generateNodePos_server=True):
        G = nx.gnm_random_graph(param['nNodes'], param['nEdges'])
        if generateNodePos_server:
            pos = graphviz_layout(G)
        self.modelData = {'nodes': [], 'edges': []}
        # store nodes in self.modelData['nodes']
        node_data = [n for n,d in G.nodes_iter(data=True)]
        for n in node_data:
            tmp= {'node_id': str(n), 'label': str(n), 
                  'size': random.uniform(param['minNodeSize'], param['maxNodeSize'])}
            if generateNodePos_server:
                tmp.update({'x': pos[n][0], 'y': pos[n][1]})
            self.modelData['nodes'].append(tmp)
        # store category information
        edgeTypes = param['edgeTypes']
        num_edgeTypes = len(edgeTypes)
        self.categories = []
        for e in edgeTypes:
             self.categories.append({'@value': e, '@label': e})
        # store edge in self.modelData['edges']
        edge_data = list(G.edges_iter(data=False))
        for e in edge_data:
            tmp = {'source': str(e[0]), 'target': str(e[1]), 
                   'strength': random.uniform(param['minEdgeStrength'], param['maxEdgeStrength']),
                   'date': 2015, 
                   'type': edgeTypes[random.randint(0,num_edgeTypes-1)]}
            self.modelData['edges'].append(tmp)
        return True
