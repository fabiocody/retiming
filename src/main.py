#!/usr/bin/env python3

import networkx as nx
from tqdm import trange
from algos import opt1, opt2, cp
from generators import gen_random_circuit, gen_correlator
from utils import load_graph, draw_graph, check_if_synchronous_circuit

from networkx.drawing.nx_pydot import write_dot


def save_graph(g):
    write_dot(g, '../graphs/tmp.dot')


if __name__ == '__main__':
    for _ in trange(1000):
        g = gen_random_circuit(N=5, E=10)
        gr1 = opt1(g)
        gr2 = opt2(g)
        cpg = cp(g)
        cpgr1 = cp(gr1)
        cpgr2 = cp(gr2)
        try:
            assert cpgr1 <= cpg
            assert cpgr2 <= cpg
        except Exception as exception:
            print(cpg, cpgr1, cpgr2)
            gr12 = opt1(g)
