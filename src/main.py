#!/usr/bin/env python3

import networkx as nx
from utils import load_graph, draw_graph, check_if_synchronous_circuit, gen_random_circuit
from algos import opt1, opt2, cp


if __name__ == '__main__':
    g = gen_random_circuit()
    draw_graph(g)
    print(f'Original clock period  = {cp(g)}')
    gr = opt2(g)
    print(f'Optimized clock period = {cp(gr)}')
    assert cp(gr) <= cp(g)
