#!/usr/bin/env python3

import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import numpy as np
from algos import cp
from utils import add_weighted_node, check_if_synchronous_circuit, w


def gen_provided_correlator(n):
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


def gen_correlator(k):
    assert k >= 1, 'k should be greater than or equal to 1'
    g = nx.DiGraph()
    add_weighted_node(g, 'h', 0)
    for i in range(k+1):
        add_weighted_node(g, f'd{i}', 3)
        if i < k:
            add_weighted_node(g, f'p{i}', 7)
    g.add_weighted_edges_from([('h', 'd0', 1)])
    g.add_weighted_edges_from([(f'd{i}', f'd{i+1}', 1) for i in range(k)])
    g.add_weighted_edges_from([(f'd{i}', f'p{i}', 0) for i in range(k)])
    g.add_weighted_edges_from([(f'd{k}', f'p{k-1}', 0)])
    g.add_weighted_edges_from([(f'p{i+1}', f'p{i}', 0) for i in range(k-1)])
    g.add_weighted_edges_from([('p0', 'h', 0)])
    return g


def gen_random_circuit(N=15, E=30):
    while True:
        g = nx.gnm_random_graph(N, E, directed=True)
        for v in g.nodes:
            g.nodes[v]['weight'] = np.random.randint(1, 3)
        g.nodes[0]['weight'] = 0
        for e in g.edges:
            g.edges[e]['weight'] = np.random.randint(3)
        if check_if_synchronous_circuit(g):
            for n in g.nodes:
                if g.in_degree(n) < 1 or not nx.has_path(g, n, 0):
                    return gen_random_circuit(N, E)
            node_weights = list(map(lambda n: g.nodes[n]['weight'], g.nodes))
            if cp(g) < max(node_weights):
                continue
            return g
