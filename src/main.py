#!/usr/bin/env python3

import big_o
import numpy as np
from algos import cp, wd, opt1, feas, opt2
from generators import gen_random_circuit


def gen_random_circuit_nodes(n):
    return gen_random_circuit(n, round(n / 8 * 11))


def gen_random_circuit_edges(n):
    return gen_random_circuit(round(n / 11 * 8), n)


def check_time_complexity():
    MIN_N = 3
    MAX_N = 200

    print('Algorithm CP  -  Expected O(E)')
    best, _ = big_o.big_o(cp, lambda n: gen_random_circuit_edges(n), min_n=MIN_N, max_n=MAX_N)
    print(' ', best, end='\n\n')

    print('Algorithm WD  -  Expected O(V^3)')
    best, _ = big_o.big_o(wd, lambda n: gen_random_circuit_nodes(n), min_n=MIN_N, max_n=MAX_N)
    print(' ', best, end='\n\n')

    print('Algorithm OPT1  -  Expected O(V^3 lg V)')
    best, _ = big_o.big_o(opt1, lambda n: gen_random_circuit_nodes(n), min_n=MIN_N, max_n=MAX_N)
    print(' ', best, end='\n\n')

    print('Algorithm FEAS  -  Expected O(VE)')
    best, _ = big_o.big_o(lambda g: feas(g, np.inf), lambda n: gen_random_circuit_nodes(n), min_n=MIN_N, max_n=MAX_N)
    print('  NODES:', best)
    best, _ = big_o.big_o(lambda g: feas(g, np.inf), lambda n: gen_random_circuit_edges(n), min_n=MIN_N, max_n=MAX_N)
    print('  EDGES:', best, end='\n\n')

    print('Algorithm OPT2  -  Expected O(VE lg V)')
    best, _ = big_o.big_o(opt2, lambda n: gen_random_circuit_nodes(n), min_n=MIN_N, max_n=MAX_N)
    print(' ', best, end='\n\n')


if __name__ == '__main__':
    check_time_complexity()
