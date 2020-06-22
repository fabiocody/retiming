#!/usr/bin/env python3

import networkx as nx
from gutils import d, w
from structures import MyTuple


def cp(g):      # O(|E|)
    zero_edges = list(filter(lambda e: w(g, e) == 0, g.edges))
    g0 = g.edge_subgraph(zero_edges)
    delta = dict()

    def __delta(g, v):
        delta_v = d(g, v)
        if g.in_degree(v) > 0:
            delta_v += max(list(map(lambda e: __delta(g, e[0]), g.in_edges(v))))
        return delta_v

    for v in nx.algorithms.dag.topological_sort(g0):
        delta[v] = __delta(g0, v)
    return max(delta.values())


def wd(g):
    g = g.copy()
    for e in g.edges:
        g.edges[e]['weight'] = MyTuple((w(g, e), -d(g, e[0])))
    sp = nx.floyd_warshall(g)
    for h in sp:
        for k in sp[h]:
            if sp[h][k] == 0:
                sp[h][k] = MyTuple([0, 0])
    W = {u: {v: sp[u][v][0] for v in g.nodes} for u in g.nodes}
    D = {u: {v: d(g, v) - sp[u][v][1] for v in g.nodes} for u in g.nodes}
    return W, D
