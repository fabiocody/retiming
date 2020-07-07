#!/usr/bin/env python3

import networkx as nx
import numpy as np
from utils import add_weighted_node, check_if_synchronous_circuit, save_graph


def gen_provided_correlator(n, save=False):
    """
    Generate a correlator circuit like the ones described in the paper.

    :param n: The values 1 or 2, depending on which correlator you want to generate.
    :param save: Whether to save the generated graph or not.
    :return: The generated graph.
    """

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
        if save:
            save_graph(g, '../graphs/correlator1.dot')
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
        if save:
            save_graph(g, '../graphs/correlator2.dot')
    else:
        raise NotImplementedError()
    return g


def gen_correlator(k, save=False):
    """
    Generate a correlator of order :math:`k`.

    :param k: The order of the correlator.
    :param save: Whether to save the generated graph or not.
    :return: The generated graph.
    """
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
    if save:
        save_graph(g, f'../graphs/correlator_k{k}.dot')
    return g


def gen_random_circuit(V=8, E=11, save=False):
    """
    Generate a random synchronous circuit.

    :param V: The number of nodes.
    :param E: The number of edges.
    :param save: If different from ``None`` or ``False``, the path where to save the generated graph.
    :return: The generated graph.
    """
    while True:
        g = nx.gnm_random_graph(V, E, directed=True)
        for v in g.nodes:
            g.nodes[v]['weight'] = np.random.randint(1, 10)
        g.nodes[0]['weight'] = 0
        for e in g.edges:
            g.edges[e]['weight'] = np.random.randint(10)
        if check_if_synchronous_circuit(g):
            if save:
                save_graph(g, save)
            return g
