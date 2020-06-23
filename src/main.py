#!/usr/bin/env python3

import networkx as nx
import gutils
from algos import retime, feas, opt1


if __name__ == '__main__':
    g = gutils.load_graph('../graphs/correlator1.dot')
    gutils.draw_graph(g)
    gr = retime(g, feas(g, 13))
    gutils.draw_graph(gr)
    gr = opt1(g)
    gutils.draw_graph(gr)
