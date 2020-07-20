#!/usr/bin/env python3

from pprint import pprint
import networkx as nx
from networkx.drawing.nx_pydot import read_dot, write_dot
import matplotlib.pyplot as plt
import numpy as np


def draw_graph(g, weights=False):
    g = nx.DiGraph(g)
    pos = nx.circular_layout(g)
    edge_weights = nx.get_edge_attributes(g, 'weight')
    node_weights = nx.get_node_attributes(g, 'weight')
    nx.draw_networkx(g, pos, font_color='white', font_size=10, labels=node_weights if weights else None)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_weights)
    plt.show()


def add_weighted_node(g, n, weight):
    g.add_node(n, weight=weight)


def load_graph(path):
    g = read_dot(path)
    for v in g.nodes:
        g.nodes[v]['weight'] = int(g.nodes[v]['weight'])
    for e in g.edges:
        g.edges[e]['weight'] = int(g.edges[e]['weight'])
    return g


def save_graph(g, path):
    g = g.copy()
    for v in g.nodes:
        g.nodes[v]['label'] = f'{v};{g.nodes[v]["weight"]}'
    for e in g.edges:
        g.edges[e]['label'] = g.edges[e]['weight']
    write_dot(g, path)


def __reconstruct_edges(g, u, v):
    """
    Compute all paths between two nodes and fix the labelling for MultiDiGraphs.

    :param g: A NetworkX (Multi)DiGraph representing a synchronous circuit.
    :param u: The first of the two nodes.
    :param v: The second of the two nodes.
    :return: The list of paths with the labels fixed.
    """
    edges = list(filter(lambda p: len(p) == 2, nx.all_simple_paths(g, u, v)))
    if isinstance(g, nx.MultiDiGraph):
        key = list(map(lambda e: e[2], g.edges))[0]
        if isinstance(key, str):
            edges = [edges[i] + [f'{i}'] for i in range(len(edges))]
        elif isinstance(key, int):
            edges = [edges[i] + [i] for i in range(len(edges))]
        else:
            raise NotImplementedError('Keys should be either strings or integers')
    elif isinstance(g, nx.DiGraph):
        pass
    else:
        raise NotImplementedError('This function only works on (Multi)DiGraph')
    return edges


def w(g, e):
    return g.edges[e]['weight']


def d(g, v):
    return g.nodes[v]['weight']


def w_path(g, p):
    wp = 0
    for i in range(len(p) - 1):
        u = p[i]
        v = p[i+1]
        edges = __reconstruct_edges(g, u, v)
        wp += min(map(lambda e: g.edges[e]['weight'], edges))
    return wp


def d_path(g, path):
    return sum(map(lambda v: g.nodes[v]['weight'], path))


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
            edges = __reconstruct_edges(g, u, v)
            min_cost = min(map(lambda e: g.edges[e]['weight'], edges))
            cost += min_cost
            if min_cost > 0:
                break
        if cost == 0:
            return False
    return True


def print_wd(m):
    rows, cols = zip(*m.keys())
    nodes = list(set(rows).union(set(cols)))
    nodes.sort()
    print('   | ', end='')
    for u in nodes:
        print(f'{str(u):>2s}', end=' ')
    print('\n---+', end='')
    for _ in nodes:
        print('---', end='')
    print()
    for u in nodes:
        print(f'{str(u):>2s} |', end=' ')
        for v in nodes:
            if (u, v) in m:
                print(f'{m[(u, v)]:>2d}', end=' ')
            else:
                print('XX', end=' ')
        print()
