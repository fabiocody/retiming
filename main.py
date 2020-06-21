#!/usr/bin/env python3

import networkx as nx
import gutils


if __name__ == '__main__':
    g = gutils.load_graph('graphs/correlator1.dot')
    gutils.draw_graph(g)
    gutils.draw_graph(g, weights=True)
    print(nx.dijkstra_path_length(g, 'h', 'd4'), '-', nx.dijkstra_path(g, 'h', 'd4'))
