#!/usr/bin/env python3

from argparse import ArgumentParser
from big_o import big_o
import numpy as np
from tqdm import trange
from algos import cp, wd, opt1, feas, opt2
from generators import gen_random_circuit
from utils import load_graph


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


def run(g):
    cpg = cp(g)
    print(f'The original graph has a clock period of {cpg}')
    print('Running algorithm OPT1')
    cpr1 = cp(opt1(g))
    print(f'The graph returned by OPT1 has a clock period of {cpr1}')
    print('Running algorithm OPT2')
    cpr2 = cp(opt2(g))
    print(f'The graph returned by OPT2 has a clock period of {cpr2}')


if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_random = subparsers.add_parser('random', help='Run the algorithms on a random graph')
    parser_random.add_argument('--nodes', '-n', type=int, default=8, help='The number of nodes (default 8)')
    parser_random.add_argument('--edges', '-e', type=int, default=11, help='The number of edges (default 11)')
    parser_file = subparsers.add_parser('file', help='Run the algorithms on a graph loaded from a provided DOT file')
    parser_file.add_argument('file', help='The DOT file from which the graph is loaded')
    args = parser.parse_args()
    if 'nodes' in args and 'edges' in args:
        print(f'Generating random graph with {args.nodes} nodes and {args.edges} edges')
        g = gen_random_circuit(args.nodes, args.edges)
        run(g)
    elif 'file' in args:
        print(f'Loading graph from {args.file}')
        g = load_graph(args.file)
        run(g)
    else:
        print('ERROR: unrecognized argument')
