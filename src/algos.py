#!/usr/bin/env python3

import networkx as nx
import numpy as np
from utils import d, w
from structures import MyTuple


def cp(g, return_delta=False):
    """
    Compute the clock period of a synchronous circuit.

    Time complexity:    :math:`O(E)`

    Space complexity:   :math:`O(V + E)`

    :param g: A NetworkX (Multi)DiGraph representing a synchronous circuit
    :param return_delta: Whether to return the computed ∆ or not (used in other algorithms)
    :return: the clock period of the given circuit
    """

    # STEP 1
    # Let G0 be the sub-graph of G that contains precisely those edges e with register count w(e) = 0.
    zero_edges = list(filter(lambda e: w(g, e) == 0, g.edges))
    g0 = nx.MultiDiGraph()
    g0.add_nodes_from(g.nodes(data=True))
    g0.add_edges_from(zero_edges)
    delta = dict()

    # STEP 2
    # By condition W2, G0 is acyclic. Perform a topological sort on G0, totally ordering its vertices so that if there
    # is an edge from vertex u to vertex v in G0, then u precedes v in the total order. Go though the vertices in the
    # order defined by the topological sort.
    for v in nx.topological_sort(g0):
        # STEP 3
        # On visiting each vertex v, compute the quantity ∆(v) as follows:
        #   a. If there is no incoming edge to v, set ∆(v) <- d(v).
        #   b. Otherwise, set ∆(v) <- d(v) + max { ∆(u) : u -e-> v and w(e) = 0 }.
        delta[v] = d(g0, v)
        if g0.in_degree(v) > 0:
            delta[v] += max(list(map(lambda e: delta[e[0]], g0.in_edges(v))))

    # STEP 4
    # The clock period is max { ∆(v) }.
    if return_delta:
        return max(delta.values()), delta
    return max(delta.values())


def wd(g):
    """
    Given a synchronous circuit G, this algorithm computes W(u, v) and D(u, v) for all u,v in V such that
    u is connected to v in G.

    Time complexity:    :math:`O(V^3)`

    Space complexity:   :math:`O(V^2)`

    :param g: A NetworkX (Multi)DiGraph representing a synchronous circuit
    :return: Matrices W and D in the form dict<(u,v), int>
    """

    # STEP 1
    # Weight each edge (u,?) in E with the ordered pair (w(e), -d(u)).
    g = g.copy()
    for e in g.edges:
        g.edges[e]['weight'] = MyTuple((w(g, e), -d(g, e[0])))

    # STEP 2
    # Using the weighting from Step 1, compute the weight of the shortest path joining each connected pair of vertices
    # by solving an all-pairs shortest-paths algorithm -- Floyd-Warshall.
    # In the all-pairs algorithm, add two weights by performing component-wise addition, and compare weights using
    # lexicographic ordering.
    sp = nx.floyd_warshall(g)
    for u in sp:
        for v in sp[u]:
            if sp[u][v] == 0:
                sp[u][v] = MyTuple((0, 0))

    # STEP 3
    # For each shortest path weight (x, y) between two vertices u and v, set W(u, v) <- x and D(u, v) <- d(v) - y.
    W = {(u, v): sp[u][v][0] for u in g.nodes for v in g.nodes if sp[u][v] != np.inf}
    D = {(u, v): d(g, v) - sp[u][v][1] for u in g.nodes for v in g.nodes if sp[u][v] != np.inf}
    return W, D


def retime(g, r):
    """
    Compute the retimed graph.

    :param g: A NetworkX (Multi)DiGraph representing a synchronous circuit
    :param r: The retiming function r: V -> Z to be applied
    :return: The retimed graph
    """
    gr = g.copy()
    for e in gr.edges:
        gr.edges[e]['weight'] = gr.edges[e]['weight'] + r[e[1]] - r[e[0]]
    return gr


def __binary_search(arr, f, g):
    """
    Perform the binary search in order to find the minimum feasible value of c inside arr.

    :param arr: The array on which to perform the binary search
    :param f: Function to be applied to g and arr[mid] (check_th7 or feas)
    :param g: A NetworkX (Multi)DiGraph representing a synchronous circuit
    :return: The minimum clock period and the corresponding retiming function
    """
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


def opt1(g):
    """
    Given a synchronous circuit G, this algorithm determines a retiming r such that the clock period of Gr is as small
    as possible.

    Time complexity:    :math:`O(V^3 \lg V)`

    Space complexity:   :math:`O(V^2)`

    :param g: A NetworkX (Multi)DiGraph representing a synchronous circuit
    :return: The retimed graph having the smallest possible clock period
    """

    # STEP 1
    # Compute W and D using Algorithm WD.
    W, D = wd(g)

    # STEP 2
    # Sort the elements in the range of D.
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

    # STEP 3
    # Binary search among the elements D(u, v) for the minimum achievable clock period. To test whether each potential
    # clock period c is feasible, apply the Bellman-Ford algorithm to determine whether the condition in Theorem 7
    # can be satisfied.
    clock, r = __binary_search(D_range, check_th7, g)

    # STEP 4
    # For the minimum achievable clock period found in Step 3, use the values for the r(v) found by the Bellman-Ford
    # algorithm as the optimal retiming.
    return retime(g, r)


def feas(g, c):
    """
    Given a synchronous circuit G and a desired clock period c, this algorithm produces a retiming r of G such that
    Gr is a synchronous circuit with clock period not greater than c, if such retiming exists.

    Time complexity:    :math:`O(VE)`

    Space complexity:   :math:`O(V + E)`

    :param g: A NetworkX (Multi)DiGraph representing a synchronous circuit
    :param c: The desired clock period
    :return: The retiming function or None if c is not feasible
    """

    # STEP 1
    # For each vertex v, set r(v) <- 0.
    r = {v: 0 for v in g.nodes}

    # STEP 2
    # Repeat |V| - 1 times.
    gr = None
    for _ in range(g.number_of_nodes() - 1):
        # STEP 2.1
        # Compute graph Gr with the existing values of r.
        gr = retime(g, r)

        # STEP 2.2
        # Run Algorithm CP on the graph Gr to determine ∆(v) for each vertex v.
        _, delta = cp(gr, return_delta=True)

        # STEP 2.3
        # For each v such that ∆(v) > c, set r(v) <- r(v) + 1
        for v in delta.keys():
            if delta[v] > c:
                r[v] += 1

    # STEP 3
    # Run Algorithm CP on the circuit Gr. If we have that cp(gr) > c, then no feasible retiming exists.
    # Otherwise, r is the desired retiming.
    clock = cp(gr)
    if clock > c:
        return None
    return r


def opt2(g):
    """
    Given a synchronous circuit G, this algorithm determines a retiming r such that the clock period of Gr is as small
    as possible.

    Time complexity:    :math:`O(VE \lg V)`

    Space complexity:   :math:`O(V^2)`

    :param g: A NetworkX (Multi)DiGraph representing a synchronous circuit
    :return: The retimed graph having the smallest possible clock period
    """

    # STEP 1
    # Compute W and D using Algorithm WD.
    W, D = wd(g)

    # STEP 2
    # Sort the elements in the range of D.
    D_range = np.unique(list(D.values()))
    D_range.sort()

    # STEP 3
    # Binary search among the elements D(u, v) for the minimum achievable clock period. To test whether each potential
    # clock period c is feasible, apply Algorithm FEAS.
    clock, r = __binary_search(D_range, feas, g)

    # STEP 4
    # For the minimum achievable clock period found in Step 3, use the values for the r(v) found by Algorithm FEAS
    # as the optimal retiming.
    return retime(g, r)
