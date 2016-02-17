# -*- coding: utf-8 -*-

from ModelVisualizer import * 
import networkx as nx
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
            print 'Column headings and parameters in the config file are inconsistent.'
            return False
        column_index = range(0,numParams)
        if column_headings:
            row_index = range(1,len(file_data))
        else:
            row_index = range(0,len(file_data))
        self.modelData = {'nodes': [], 'edges': []}
        # load node_data from xml configuration file
        node_data = self.config_obj['model']['data']['node_config']['node']
        _node_keys = ['@node_id', '@label', '@size', '@x', '@y']
        self.node_keys = [key.translate(None, '@') for key in _node_keys]
        
        if len(node_data) == 0:
            print 'No node data found in the configuration file'
            return False
        for node in node_data:
            tmp = {}
            for i in range(len(self.node_keys)):
                value = node[_node_keys[i]]
                if self.is_number(value):
                    value = ast.literal_eval(value)
                tmp.update({self.node_keys[i]: value})
            self.modelData['nodes'].append(tmp)
        # load the connection_data from the csv data file
        for row in row_index:
            tmp = {};
            for col in column_index:
                value = file_data[row][col]
                if self.is_number(value):
                    value = ast.literal_eval(value)
                # read the data from the file
                tmp.update({self.param_keys[col]:value})
            self.modelData['edges'].append(tmp)
        if len(self.modelData['edges']) == 0:
            return False
        # for large networks we should provide node positions
        # if no node positions are provided, d3plus computes them client-side
        self.generateNodePositions = False
        generateNodePos_server = False # set to true if server is to generate node positions
        if self.modelData['nodes'][0]['x'] == '':
            if generateNodePos_server == True:
                # create an empty graph with no nodes and no edges
                G = nx.Graph()
                # add nodes to the graph
                for node in self.modelData['nodes']:
                    G.add_node(node['node_id'])
                # add edges (links) to the graph
                for edge in self.modelData['edges']:
                    G.add_edge(edge['source'], edge['target'])
                # Compute node positions
                pos= nx.graphviz_layout(G)
                # store the node positions
                for node in self.modelData['nodes']:
                    node['x'] = pos[node['node_id']][0]
                    node['y'] = pos[node['node_id']][1]
            else:
                self.generateNodePositions = True
        return True

    def render_plot(self):
        self.js = render_template('dynamic_js/network.js', conf_obj=self.config_obj,
                        categories=self.categories, modelData=self.modelData,
                        generateNodePositions = self.generateNodePositions)  
        self.plot = render_template('ModelVisualizer/network.html', js = self.js, 
                        modelData = self.modelData, categories=self.categories)
        return True

    def debug_mode(self, param, generateNodePos_server = True):
        G = nx.gnm_random_graph(param['nNodes'], param['nEdges'])
        self.generateNodePositions = True # d3plus will generate node positions
        if generateNodePos_server:
            self.generateNodePositions = False
            pos = nx.graphviz_layout(G)
        self.modelData = {'nodes': [], 'edges': []}
        # store nodes in self.modelData['nodes']
        node_data = [n for n,d in G.nodes_iter(data=True)]
        for n in node_data:
            tmp= {'node_id': str(n), 'label': str(n), 
                  'size': random.uniform(param['minNodeSize'], param['maxNodeSize'])}
            if generateNodePos_server:
                tmp.update({'x': pos[n][0], 'y': pos[n][1]})
            else:
                tmp.update({'x': '', 'y': ''})
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
