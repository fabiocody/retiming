#!/usr/bin/env python3

import networkx as nx


def cp(g):      # O(|E|)
    zero_edges = list(filter(lambda e: g.edges[e]['weight'] == 0, g.edges))
    g0 = g.edge_subgraph(zero_edges)
    delta = dict()

    def __delta(g, v):
        delta_v = g.nodes[v]['weight']
        if g.in_degree(v) > 0:
            delta_v += max(list(map(lambda e: __delta(g, e[0]), g.in_edges(v))))
        return delta_v

    for v in nx.algorithms.dag.topological_sort(g0):
        delta[v] = __delta(g0, v)
    return max(delta.values())
