#!/usr/bin/env python3

import networkx as nx
import numpy as np
from gutils import d, w, wd2numpy
from structures import MyTuple


def cp(g, return_delta=False):      # O(|E|)
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
    if return_delta:
        return max(delta.values()), delta
    return max(delta.values())


def wd(g):      # O(|V|^3)
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


def retime(g, r):
    gr = g.copy()
    for e in gr.edges:
        gr.edges[e]['weight'] = gr.edges[e]['weight'] + r[e[1]] - r[e[0]]
    return gr


def opt1(g):    # O(|V|^3 lg|V|)
    W, D = wd(g)
    D_range = np.unique(wd2numpy(D))
    D_range.sort()
    root = 'root'

    def check_th7(edges, nodes, c):
        bfg = nx.MultiDiGraph()
        bfg.add_weighted_edges_from([(e[1], e[0], w(g, e)) for e in edges])
        bfg.add_weighted_edges_from([(v, u, W[u][v]-1)
                                     for u in nodes for v in nodes
                                     if D[u][v] > c and not (D[u][v] - d(g, v) > c or D[u][v] - d(g, u) > c)])
        bfg.add_weighted_edges_from([(root, n, 0) for n in bfg.nodes])
        try:
            return nx.single_source_bellman_ford_path_length(bfg, root)
        except nx.exception.NetworkXUnbounded:
            return None

    def binary_search(arr):
        def bs_rec(low, high, prev_mid=None, prev_x=None):
            if high >= low:
                mid = (high + low) // 2
                x = check_th7(g.edges, g.nodes, arr[mid])
                if x is None:
                    return bs_rec(mid+1, high, prev_mid, prev_x)
                else:
                    return bs_rec(low, mid-1, mid, x)
            else:
                return arr[prev_mid], prev_x
        return bs_rec(0, len(arr)-1)

    _, r = binary_search(D_range)
    return retime(g, r)


def feas(g, c):     # O(|V||E|)
    r = {v: 0 for v in g.nodes}
    gr = None
    for _ in range(g.number_of_nodes() - 1):
        gr = retime(g, r)
        _, delta = cp(gr, return_delta=True)
        for v in delta.keys():
            if delta[v] > c:
                r[v] += 1
    clock = cp(gr)
    if clock > c:
        return None
    else:
        return r

