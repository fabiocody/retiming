#!/usr/bin/env python3

import networkx as nx
from networkx.drawing.nx_pydot import write_dot, read_dot
import numpy as np
import matplotlib.pyplot as plt


def draw_graph(g, weights=False):
    g = nx.DiGraph(g)
    pos = nx.shell_layout(g)
    edge_weights = nx.get_edge_attributes(g, 'weight')
    node_weights = nx.get_node_attributes(g, 'weight')
    nx.draw_networkx(g, pos, font_color='white', font_size=10, node_shape='s', labels=node_weights if weights else None)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_weights)
    plt.show()


def add_weighted_node(g, n, w):
    g.add_node(n, weight=w)


def gen_correlator(n):
    g = nx.MultiDiGraph()
    add_weighted_node(g, 'h', 0)
    add_weighted_node(g, 'd0', 3)
    add_weighted_node(g, 'd1', 3)
    add_weighted_node(g, 'd2', 3)
    add_weighted_node(g, 'd3', 3)
    add_weighted_node(g, 'p0', 7)
    add_weighted_node(g, 'p1', 7)
    add_weighted_node(g, 'p2', 7)
    if n == 1:
        g.add_weighted_edges_from([
            ('h', 'd0', 1),
            ('d0', 'd1', 1),
            ('d0', 'p0', 0),
            ('d1', 'd2', 1),
            ('d1', 'p1', 0),
            ('d2', 'd3', 1),
            ('d2', 'p2', 0),
            ('d3', 'p2', 0),
            ('p2', 'p1', 0),
            ('p1', 'p0', 0),
            ('p0', 'h', 0)
        ])
        write_dot(g, '../graphs/correlator1.dot')
    elif n == 2:
        g.add_weighted_edges_from([
            ('h', 'd0', 1),
            ('d0', 'd1', 1),
            ('d0', 'p0', 0),
            ('d1', 'd2', 0),
            ('d1', 'p1', 0),
            ('d2', 'd3', 1),
            ('d2', 'p2', 0),
            ('d3', 'p2', 0),
            ('p2', 'p1', 1),
            ('p1', 'p0', 0),
            ('p0', 'h', 0)
        ])
        write_dot(g, '../graphs/correlator2.dot')
    else:
        raise NotImplementedError()
    return g


def load_graph(path):
    g = read_dot(path)
    nodes = g.nodes(data=True)
    for e in g.edges:
        for v in e[0:2]:
            v = nodes[v]
            v['weight'] = int(v['weight'])
        g.edges[e]['weight'] = int(g.edges[e]['weight'])
    return g


def w(g, e):
    return g.edges[e]['weight']


def d(g, v):
    return g.nodes[v]['weight']


def wd2numpy(m):
    lists = [list(m[k].values()) for k in m]
    return np.array(lists)


def print_correlator_WD(W, D):
    order = ['h', 'd0', 'd1', 'd2', 'd3', 'p2', 'p1', 'p0']
    for u in order:
        for v in order:
            print(W[u][v], end=' ')
        print()
    print()
    for u in order:
        for v in order:
            print(f'{D[u][v]:2d}', end=' ')
        print()


def check_if_synchronous_circuit(g):
    # D1: the propagation delay d(v) is non-negative for each vertex v
    for v in g.nodes:
        if g.nodes[v]['weight'] < 0:
            return False
    # W1: the register count w(e) is a non-negative integer for each edge e
    for e in g.edges:
        if g.edges[e]['weight'] < 0:
            return False
    # W2: in any directed cycle of G, there is some edge with strictly positive register count
    g = g.copy()
    stop = False
    while not stop:
        try:
            cycle = nx.find_cycle(g)
            condition = False
            for e in cycle:
                if g.edges[e]['weight'] > 0:
                    condition = True
            if not condition:
                return False
            g.remove_edges_from(cycle)
        except nx.exception.NetworkXNoCycle:
            stop = True
    return True


def gen_random_circuit(n=15, e=20):
    while True:
        try:
            g = nx.gnm_random_graph(n, e, directed=True)
            for v in g.nodes:
                g.nodes[v]['weight'] = np.random.randint(5)
            for e in g.edges:
                g.edges[e]['weight'] = np.random.randint(5)
            if check_if_synchronous_circuit(g):
                return g
        except:
            pass
