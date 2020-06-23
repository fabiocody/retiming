#!/usr/bin/env python3

import networkx as nx
from tqdm import trange
from utils import load_graph, draw_graph, check_if_synchronous_circuit, gen_random_circuit
from algos import opt1, opt2, cp

from networkx.drawing.nx_pydot import write_dot


if __name__ == '__main__':
    '''for _ in trange(1000):
        g = gen_random_circuit(N=5, E=10)
        gr = opt1(g)
        cpgr = cp(gr)
        cpg = cp(g)
        assert cpgr <= cpg'''
    g = load_graph('../graphs/non-working2.dot')
    gr = opt1(g)
    cpg = cp(g)
    cpgr = cp(gr)
    assert cpgr <= cpg
