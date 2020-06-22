#!/usr/bin/env python3

import networkx as nx
import numpy as np
from gutils import d, w, wd2numpy
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


def opt1(g):
    W, D = wd(g)
    D_np = wd2numpy(D)
    D_range = np.unique(D_np)
    D_range.sort()

    root = 'root'

    def check_th7(edges, nodes, c):
        bfg = nx.MultiDiGraph()
        bfg.add_weighted_edges_from([(e[1], e[0], w(g, e)) for e in edges])
        bfg.add_weighted_edges_from([(v, u, W[u][v]-1) for u in nodes for v in nodes if D[u][v] > c])
        bfg.add_weighted_edges_from([(root, n, 0) for n in bfg.nodes])
        try:
            sp = nx.single_source_bellman_ford_path_length(bfg, root)
            return sp
        except nx.exception.NetworkXUnbounded:
            return None

    def binary_search(arr):
        def bs_rec(arr, low, high, prev_mid=None, prev_x=None):
            if high >= low:
                mid = (high + low) // 2
                x = check_th7(g.edges, g.nodes, arr[mid])
                if x is None:
                    return bs_rec(arr, mid+1, high, prev_mid, prev_x)
                else:
                    return bs_rec(arr, low, mid-1, mid, x)
            else:
                return arr[prev_mid], prev_x
        clock, r = bs_rec(arr, 0, len(arr)-1)
        del r[root]
        return clock, r

    clock, r = binary_search(D_range)

    gr = g.copy()
    # TODO: apply retiming
