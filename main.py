#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt

import gutils


if __name__ == '__main__':
    g = nx.DiGraph()
    gutils.add_weighted_node(g, 1, 2)
    gutils.add_weighted_node(g, 2, 1)
    gutils.add_weighted_node(g, 3, 1.5)
    gutils.add_weighted_node(g, 42, 24)
    g.add_weighted_edges_from([(1, 2, 0.5), (2, 3, 0.75), (3, 1, 0), (1, 42, 2)])
    gutils.draw_graph(g)
    gutils.draw_graph(g, weights=True)
