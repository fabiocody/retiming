#!/usr/bin/env python3

import networkx as nx
import numpy as np
from utils import d, w
from structures import MyTuple


def cp(g, return_delta=False):      # O(|E|)
    zero_edges = list(filter(lambda e: w(g, e) == 0, g.edges))
    if len(zero_edges) == 0:
        clock = max(map(lambda n: g.nodes[n]['weight'], g.nodes))
        if return_delta:
            return clock, {v: 0 for v in g.nodes}
        return clock
    g0 = g.edge_subgraph(zero_edges)
    delta = dict()
    for v in nx.topological_sort(g0):
        delta[v] = d(g0, v)
        if g0.in_degree(v) > 0:
            delta[v] += max(list(map(lambda e: delta[e[0]], g0.in_edges(v))))
    if return_delta:
        return max(delta.values()), delta
    return max(delta.values())


def wd(g):      # O(|V|^3)
    g = g.copy()
    for e in g.edges:
        g.edges[e]['weight'] = MyTuple((w(g, e), -d(g, e[0])))
    sp = nx.floyd_warshall(g)
    for u in sp:
        for v in sp[u]:
            if sp[u][v] == 0:
                sp[u][v] = MyTuple((0, 0))
    W = {(u, v): sp[u][v][0] for u in g.nodes for v in g.nodes if sp[u][v] != np.inf}
    D = {(u, v): d(g, v) - sp[u][v][1] for u in g.nodes for v in g.nodes if sp[u][v] != np.inf}
    return W, D


def retime(g, r):
    gr = g.copy()
    for e in gr.edges:
        try:
            gr.edges[e]['weight'] = gr.edges[e]['weight'] + r[e[1]] - r[e[0]]
        except Exception as exception:
            print(exception)
            return g
    return gr


def __binary_search(arr, f, g):
    def bs_rec(low, high, prev_mid=None, prev_x=None):
        if high >= low:
            mid = (high + low) // 2
            x = f(g, arr[mid])
            if x is None:
                return bs_rec(mid+1, high, prev_mid, prev_x)
            else:
                return bs_rec(low, mid-1, mid, x)
        else:
            return arr[prev_mid], prev_x
    return bs_rec(0, len(arr)-1)


def opt1(g):    # O(|V|^3 lg|V|)
    W, D = wd(g)
    D_range = np.unique(list(D.values()))
    D_range.sort()

    def check_th7(g, c):
        bfg = nx.MultiDiGraph()
        bfg.add_weighted_edges_from([(e[1], e[0], w(g, e)) for e in g.edges])
        bfg.add_weighted_edges_from([(v, u, W[u, v]-1)
                                     for u in g.nodes for v in g.nodes
                                     if (u, v) in W and (u, v) in D and
                                     D[u, v] > c and not (D[u, v] - d(g, v) > c or D[u, v] - d(g, u) > c)])
        root = 'root'
        bfg.add_weighted_edges_from([(root, n, 0) for n in bfg.nodes])
        try:
            return nx.single_source_bellman_ford_path_length(bfg, root)
        except nx.exception.NetworkXUnbounded:
            return None

    clock, r = __binary_search(D_range, check_th7, g)
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


def opt2(g):        # O(|V||E| lg|V|)
    W, D = wd(g)
    D_range = np.unique(list(D.values()))
    D_range.sort()
    clock, r = __binary_search(D_range, feas, g)
    if r is not None:
        return retime(g, r)
    else:
        return g
