#!/usr/bin/env python3

import networkx as nx
import gutils
from algos import cp


if __name__ == '__main__':
    g = gutils.load_graph('../graphs/correlator1.dot')
    clock_period = cp(g)
    print(f'clock_period = {clock_period}')
