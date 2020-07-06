#!/usr/bin/env python3

from big_o import big_o
import numpy as np
from tqdm import trange
from algos import cp, wd, opt1, feas, opt2
from generators import gen_random_circuit


def check_time_complexity():
    MIN_N = 10
    MAX_N = 100
    N_MEASURES = 46
    N_TIMINGS = 3

    def gen_random_circuit_nodes(n):
        n_edges = round(n / 8 * 11)
        # print(f'Generating circuit with {n} vertices and {n_edges} edges...')
        return gen_random_circuit(n, n_edges)

    def gen_random_circuit_edges(n):
        n_nodes = round(n / 11 * 8)
        # print(f'Generating circuit with {n_nodes} vertices and {n} edges...')
        return gen_random_circuit(n_nodes, n)

    print('Algorithm CP  -  Expected O(E)')
    best, _ = big_o(cp, gen_random_circuit_edges,
                    min_n=MIN_N, max_n=MAX_N,
                    n_measures=N_MEASURES, n_timings=N_TIMINGS)
    print(best, end='\n\n')

    print('Algorithm WD  -  Expected O(V^3)')
    best, _ = big_o(wd, gen_random_circuit_nodes,
                    min_n=MIN_N, max_n=MAX_N,
                    n_measures=N_MEASURES, n_timings=N_TIMINGS)
    print(best, end='\n\n')

    print('Algorithm OPT1  -  Expected O(V^3 log V)')
    best, _ = big_o(opt1, gen_random_circuit_nodes,
                    min_n=MIN_N, max_n=MAX_N,
                    n_measures=N_MEASURES, n_timings=N_TIMINGS)
    print(best, end='\n\n')

    print('Algorithm FEAS  -  Expected O(VE)')
    best, _ = big_o(lambda g: feas(g, np.inf), gen_random_circuit_nodes,
                    min_n=MIN_N, max_n=MAX_N,
                    n_measures=N_MEASURES, n_timings=N_TIMINGS)
    print('NODES:', best)
    best, _ = big_o(lambda g: feas(g, np.inf), gen_random_circuit_edges,
                    min_n=MIN_N, max_n=MAX_N,
                    n_measures=N_MEASURES, n_timings=N_TIMINGS)
    print('EDGES:', best, end='\n\n')

    print('Algorithm OPT2  -  Expected O(VE log V)')
    best, _ = big_o(opt2, gen_random_circuit_nodes,
                    min_n=MIN_N, max_n=MAX_N,
                    n_measures=N_MEASURES, n_timings=N_TIMINGS)
    print(best, end='\n\n')


def random_test(n=10000):
    for _ in trange(n):
        V = np.random.randint(5, 30)
        E = np.random.randint(5, 30)
        g = gen_random_circuit(V, E)
        cpg = cp(g)
        cpr1 = cp(opt1(g))
        cpr2 = cp(opt2(g))
        assert cpr1 == cpr2 and cpr1 <= cpg and cpr2 <= cpg


if __name__ == '__main__':
    check_time_complexity()
