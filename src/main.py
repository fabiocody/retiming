#!/usr/bin/env python3

import big_o
import numpy as np
from algos import cp, wd, opt1, feas, opt2
from generators import gen_random_circuit


def check_time_complexity():
    MIN_N = 5
    MAX_N = 250

    def gen_random_circuit_nodes(n):
        n_edges = round(n / 8 * 11)
        # n_edges = np.random.randint(round(0.5 * n), round(1.5 * n))
        return gen_random_circuit(n, n_edges)

    def gen_random_circuit_edges(n):
        n_nodes = round(n / 11 * 8)
        # n_nodes = np.random.randint(round(0.5 * n), round(1.5 * n))
        return gen_random_circuit(n_nodes, n)

    print('Algorithm CP  -  Expected O(E)')
    best, _ = big_o.big_o(cp, gen_random_circuit_edges, min_n=MIN_N, max_n=MAX_N)
    print(' ', best, end='\n\n')

    print('Algorithm WD  -  Expected O(V^3)')
    best, _ = big_o.big_o(wd, gen_random_circuit_nodes, min_n=MIN_N, max_n=MAX_N)
    print(' ', best, end='\n\n')

    print('Algorithm OPT1  -  Expected O(V^3 lg V)')
    best, _ = big_o.big_o(opt1, gen_random_circuit_nodes, min_n=MIN_N, max_n=MAX_N)
    print(' ', best, end='\n\n')

    print('Algorithm FEAS  -  Expected O(VE)')
    best, _ = big_o.big_o(lambda g: feas(g, np.inf), gen_random_circuit_nodes, min_n=MIN_N, max_n=MAX_N)
    print('  NODES:', best)
    best, _ = big_o.big_o(lambda g: feas(g, np.inf), gen_random_circuit_edges, min_n=MIN_N, max_n=MAX_N)
    print('  EDGES:', best, end='\n\n')

    print('Algorithm OPT2  -  Expected O(VE lg V)')
    best, _ = big_o.big_o(opt2, gen_random_circuit_nodes, min_n=MIN_N, max_n=MAX_N)
    print(' ', best, end='\n\n')


if __name__ == '__main__':
    check_time_complexity()
