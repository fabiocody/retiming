#!/usr/bin/env python3

import networkx as nx
from networkx.drawing.nx_pydot import read_dot, write_dot
import numpy as np
import matplotlib.pyplot as plt


def draw_graph(g, weights=False):
    g = nx.DiGraph(g)
    pos = nx.circular_layout(g)
    edge_weights = nx.get_edge_attributes(g, 'weight')
    node_weights = nx.get_node_attributes(g, 'weight')
    nx.draw_networkx(g, pos, font_color='white', font_size=10, labels=node_weights if weights else None)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_weights)
    plt.show()


def add_weighted_node(g, n, w):
    g.add_node(n, weight=w)


def load_graph(path):
    g = read_dot(path)
    nodes = g.nodes(data=True)
    for e in g.edges:
        for v in e[0:2]:
            v = nodes[v]
            try:
                v['weight'] = int(v['weight'])
            except KeyError:
                pass
        g.edges[e]['weight'] = int(g.edges[e]['weight'])
    return g


def save_graph(g, path):
    g = g.copy()
    for e in g.edges:
        g.edges[e]['label'] = g.edges[e]['weight']
    write_dot(g, path)


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


def get_g0(g):
    zero_edges = list(filter(lambda e: w(g, e) == 0, g.edges))
    return g.edge_subgraph(zero_edges)


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
    for nodes in nx.simple_cycles(g):
        cost = 0
        for i in range(len(nodes)):
            u = nodes[i]
            v = nodes[(i + 1) % len(nodes)]
            paths = list(filter(lambda p: len(p) == 2, nx.all_simple_paths(g, u, v)))
            if isinstance(g, nx.MultiDiGraph):
                key = list(map(lambda e: e[2], g.edges))[0]
                if isinstance(key, str):
                    edges = [paths[i] + [f'{i}'] for i in range(len(paths))]
                elif isinstance(key, int):
                    edges = [paths[i] + [i] for i in range(len(paths))]
                else:
                    raise NotImplementedError('Keys should be either strings or integers')
            elif isinstance(g, nx.DiGraph):
                edges = paths
            else:
                raise NotImplementedError('This function only works on (Multi)DiGraph')
            min_cost = min(map(lambda e: g.edges[e]['weight'], edges))
            cost += min_cost
            if min_cost > 0:
                break
        if cost == 0:
            return False
    return True
