#!/usr/bin/env python3

import networkx as nx
import gutils
from algos import wd


if __name__ == '__main__':
    g = gutils.load_graph('../graphs/correlator1.dot')
    gutils.draw_graph(g)
    W, D = wd(g)
    gutils.print_correlator_WD(W, D)

