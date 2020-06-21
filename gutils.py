#!/usr/bin/env python3


import networkx as nx
from networkx.drawing.nx_pydot import write_dot, read_dot
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


def gen_correlator1():
    g = nx.DiGraph()
    add_weighted_node(g, 'h', 0)
    add_weighted_node(g, 'd1', 3)
    add_weighted_node(g, 'd2', 3)
    add_weighted_node(g, 'd3', 3)
    add_weighted_node(g, 'd4', 3)
    add_weighted_node(g, 'p1', 7)
    add_weighted_node(g, 'p2', 7)
    add_weighted_node(g, 'p3', 7)
    g.add_weighted_edges_from([
        ('h', 'd1', 1),
        ('d1', 'd2', 1),
        ('d1', 'p1', 0),
        ('d2', 'd3', 1),
        ('d2', 'p2', 0),
        ('d3', 'd4', 1),
        ('d3', 'p3', 0),
        ('d4', 'p3', 0),
        ('p3', 'p2', 0),
        ('p2', 'p1', 0),
        ('p1', 'h', 0)
    ])
    write_dot(g, 'graphs/correlator1.dot')
    return g


def gen_correlator2():
    g = nx.DiGraph()
    add_weighted_node(g, 'h', 0)
    add_weighted_node(g, 'd1', 3)
    add_weighted_node(g, 'd2', 3)
    add_weighted_node(g, 'd3', 3)
    add_weighted_node(g, 'd4', 3)
    add_weighted_node(g, 'p1', 7)
    add_weighted_node(g, 'p2', 7)
    add_weighted_node(g, 'p3', 7)
    g.add_weighted_edges_from([
        ('h', 'd1', 1),
        ('d1', 'd2', 1),
        ('d1', 'p1', 0),
        ('d2', 'd3', 0),
        ('d2', 'p2', 0),
        ('d3', 'd4', 1),
        ('d3', 'p3', 0),
        ('d4', 'p3', 0),
        ('p3', 'p2', 1),
        ('p2', 'p1', 0),
        ('p1', 'h', 0)
    ])
    write_dot(g, 'graphs/correlator2.dot')
    return g


def load_graph(path):
    g = nx.DiGraph(read_dot(path))
    nodes = g.nodes(data=True)
    for e in g.edges:
        for v in e:
            v = nodes[v]
            v['weight'] = int(v['weight'])
        g.edges[e]['weight'] = int(g.edges[e]['weight'])
    return g
