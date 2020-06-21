#!/usr/bin/env python3

import networkx as nx
import gutils


if __name__ == '__main__':
    g = gutils.load_graph('../graphs/correlator1.dot')
    gutils.draw_graph(g)
    g = gutils.load_graph('../graphs/correlator2.dot')
    gutils.draw_graph(g)
