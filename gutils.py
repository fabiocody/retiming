#!/usr/bin/env python3


import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(g, weights=False):
    pos = nx.planar_layout(g)
    edge_weights = nx.get_edge_attributes(g, 'weight')
    node_weights = nx.get_node_attributes(g, 'weight')
    nx.draw_networkx(g, pos, font_color='white', font_size=10, node_shape='s', labels=node_weights if weights else None)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_weights)
    plt.show()


def add_weighted_node(g, n, w):
    g.add_node(n, weight=w)
