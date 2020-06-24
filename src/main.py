#!/usr/bin/env python3

import networkx as nx
from algos import opt1, opt2, cp, wd
from generators import gen_random_circuit, gen_correlator
from utils import load_graph, draw_graph, check_if_synchronous_circuit, save_graph


if __name__ == '__main__':
    i = 0
    while True:
        print(f'\r{i}', end='')
        g = gen_random_circuit(N=5, E=10)
        gr1 = opt1(g)
        gr2 = opt2(g)
        cpg = cp(g)
        cpgr1 = cp(gr1)
        cpgr2 = cp(gr2)
        if cpgr1 > cpg or cpgr2 > cpg:
            print('\n', cpg, cpgr1, cpgr2)
            wd(g)
            gr12 = opt1(g)
        i += 1
