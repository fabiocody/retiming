#!/usr/bin/env python3

import networkx as nx
import numpy as np
from unittest import TestCase
from algos import cp, wd, opt1, feas, opt2
from generators import gen_correlator, gen_random_circuit
from structures import MyTuple
from utils import load_graph, check_if_synchronous_circuit, w_path, d_path, d, add_weighted_node


def wd2numpy_correlator(m):
    """
    Transform matrix :math:`W` or :math:`D` of correlator1 into a 2D numpy array.

    :param m: matrix :math:`W` or :math:`D` as returned by *Algorithm WD*.
    :return: the numpy version of the provided matrix.
    """
    order = ['h', 'd0', 'd1', 'd2', 'd3', 'p2', 'p1', 'p0']
    lists = [[] for _ in order]
    for u in order:
        for v in order:
            lists[order.index(u)].append(m[u, v])
    return np.array(lists)


class Tests(TestCase):

    def test_correlator1_cp(self):
        """
        Check that the clock period of correlator1 is 24.
        """
        g = load_graph('../graphs/correlator1.dot')
        clock_period = cp(g)
        self.assertEqual(clock_period, 24)

    def test_correlator2_cp(self):
        """
        Check that the clock period of correlator2 is 17.
        """
        g = load_graph('../graphs/correlator2.dot')
        clock_period = cp(g)
        self.assertEqual(clock_period, 17)

    def test_correlator1_wd(self):
        """
        Check that matrices :math:`W` and :math:`D` of correlator1 correspond to the ones stated in the paper.
        """
        W_test = np.array([
            [0, 1, 2, 3, 4, 3, 2, 1],
            [0, 0, 1, 2, 3, 2, 1, 0],
            [0, 1, 0, 1, 2, 1, 0, 0],
            [0, 1, 2, 0, 1, 0, 0, 0],
            [0, 1, 2, 3, 0, 0, 0, 0],
            [0, 1, 2, 3, 4, 0, 0, 0],
            [0, 1, 2, 3, 4, 3, 0, 0],
            [0, 1, 2, 3, 4, 3, 2, 0]
        ])
        D_test = np.array([
            [0, 3, 6, 9, 12, 16, 13, 10],
            [10, 3, 6, 9, 12, 16, 13, 10],
            [17, 20, 3, 6, 9, 13, 10, 17],
            [24, 27, 30, 3, 6, 10, 17, 24],
            [24, 27, 30, 33, 3, 10, 17, 24],
            [21, 24, 27, 30, 33, 7, 14, 21],
            [14, 17, 20, 23, 26, 30, 7, 14],
            [7, 10, 13, 16, 19, 23, 20, 7]
        ])
        g = load_graph('../graphs/correlator1.dot')
        W, D = wd(g)
        W = wd2numpy_correlator(W)
        D = wd2numpy_correlator(D)
        self.assertTrue((W == W_test).all())
        self.assertTrue((D == D_test).all())

    def test_correlator1_opt1(self):
        """
        Check that *Algorithm OPT1* applied to correlator1 produces a clock period of 13.
        """
        g = load_graph('../graphs/correlator1.dot')
        gr = opt1(g)
        self.assertEqual(cp(gr), 13)

    def test_correlator2_opt1(self):
        """
        Check that *Algorithm OPT1* applied to correlator2 produces a clock period of 13.
        """
        g = load_graph('../graphs/correlator2.dot')
        gr = opt1(g)
        self.assertEqual(cp(gr), 13)

    def test_correlator1_feas(self):
        """
        Check that 13 is a feasible clock period for correlator1 with *Algorithm FEAS*.
        """
        g = load_graph('../graphs/correlator1.dot')
        r = feas(g, 13)
        self.assertIsNotNone(r)

    def test_correlator2_feas(self):
        """
        Check that 13 is a feasible clock period for correlator2 with *Algorithm FEAS*.
        """
        g = load_graph('../graphs/correlator2.dot')
        r = feas(g, 13)
        self.assertIsNotNone(r)

    def test_correlator1_opt2(self):
        """
        Check that *Algorithm OPT2* applied to correlator1 produces a clock period of 13.
        """
        g = load_graph('../graphs/correlator1.dot')
        gr = opt2(g)
        self.assertEqual(cp(gr), 13)

    def test_correlator2_opt2(self):
        """
        Check that *Algorithm OPT2* applied to correlator2 produces a clock period of 13.
        """
        g = load_graph('../graphs/correlator2.dot')
        gr = opt2(g)
        self.assertEqual(cp(gr), 13)

    def test_MyTuple(self):
        """
        Check that ``MyTuple`` behaves as expected.
        """
        t1 = MyTuple((1, 2, 3))
        t2 = MyTuple((1, 2, 3))
        t3 = MyTuple((2, 3, 4))
        t4 = MyTuple((0, 1, 2))
        t5 = MyTuple((0, 1, 2, 3, 4))
        self.assertEqual(t1+t1, MyTuple((2, 4, 6)))
        self.assertEqual(t1+1, t3)
        self.assertEqual(1+t1, t3)
        self.assertRaises(NotImplementedError, lambda a, b: a+b, t1, [1, 2])
        self.assertRaises(NotImplementedError, lambda a, b: a + b, [1, 2], t1)
        self.assertEqual(t1, t2)
        self.assertLess(t1, t3)
        self.assertGreater(t1, t4)
        self.assertLess(t2, t3)
        self.assertGreater(t2, t4)
        self.assertGreater(t3, t4)
        self.assertFalse(t1 < t2)
        self.assertFalse(t1 < [1, 2])
        self.assertGreater(t1, 0)
        self.assertFalse(t1 > [1, 2])
        self.assertLessEqual(t1, t2)
        self.assertFalse(t3 <= t1)
        self.assertLessEqual(t1, 3)
        self.assertFalse(t1 <= 2)
        self.assertFalse(t1 <= [1, 2])
        self.assertFalse(t1 >= t3)
        self.assertGreaterEqual(t3, t1)
        self.assertGreaterEqual(t3, 2)
        self.assertFalse(t3 >= 4)
        self.assertFalse(t1 >= [1, 2])
        self.assertFalse(t1 == t3)
        self.assertFalse(t1 == t5)
        self.assertFalse(t1 == [1, 2])

    def test_correlator1_synchronous_circuit(self):
        """
        Check that correlator1 is actually a synchronous circuit.
        """
        g = load_graph('../graphs/correlator1.dot')
        self.assertTrue(check_if_synchronous_circuit(g))

    def test_correlator2_synchronous_circuit(self):
        """
        Check that correlator2 is actually a synchronous circuit.
        """
        g = load_graph('../graphs/correlator2.dot')
        self.assertTrue(check_if_synchronous_circuit(g))

    def test_correlator1_retimed_opt1_synchronous_circuit(self):
        """
        Check that the circuit retimed with *Algorithm OPT1* starting from correlator1 is actually a synchronous circuit.
        """
        g = load_graph('../graphs/correlator1.dot')
        gr = opt1(g)
        self.assertTrue(check_if_synchronous_circuit(gr))

    def test_correlator1_retimed_opt2_synchronous_circuit(self):
        """
        Check that the circuit retimed with *Algorithm OPT2* starting from correlator1 is actually a synchronous circuit.
        """
        g = load_graph('../graphs/correlator1.dot')
        gr = opt2(g)
        self.assertTrue(check_if_synchronous_circuit(gr))

    def test_correlator2_retimed_opt1_synchronous_circuit(self):
        """
        Check that the circuit retimed with *Algorithm OPT1* starting from correlator2 is actually a synchronous circuit.
        """
        g = load_graph('../graphs/correlator2.dot')
        gr = opt1(g)
        self.assertTrue(check_if_synchronous_circuit(gr))

    def test_correlator2_retimed_opt2_synchronous_circuit(self):
        """
        Check that the circuit retimed with *Algorithm OPT2* starting from correlator2 is actually a synchronous circuit.
        """
        g = load_graph('../graphs/correlator2.dot')
        gr = opt2(g)
        self.assertTrue(check_if_synchronous_circuit(gr))

    def test_correlators(self):
        """
        Check that all the correlators of order :math:`1 \leq k \leq 15` optimized either with *Algorithm OPT1* or
        *OPT2* have a clock period not greater that 14.
        """
        for i in range(1, 16):
            g = gen_correlator(i)
            gr1 = opt1(g)
            gr2 = opt2(g)
            self.assertLessEqual(cp(gr1), 14)
            self.assertLessEqual(cp(gr2), 14)

    def test_random_wd(self):
        """
        Check that the computed :math:`W` and :math:`D` matrices correspond to the definition.
        """
        for _ in range(10):
            g = gen_random_circuit()
            W, D = wd(g)
            for u in g.nodes:
                for v in g.nodes:
                    if nx.has_path(g, u, v):
                        if u == v:
                            self.assertEqual(W[u, v], 0)
                            self.assertEqual(D[u, v], d(g, u))
                        else:
                            self.assertEqual(W[u, v], min([w_path(g, p) for p in nx.all_simple_paths(g, u, v)]))
                            self.assertEqual(D[u, v], max([d_path(g, p) for p in nx.all_simple_paths(g, u, v) if w_path(g, p) == W[u, v]]))
                    else:
                        self.assertFalse((u, v) in W)
                        self.assertFalse((u, v) in D)

    def test_random_opt1(self):
        """
        Check that *Algorithm OPT1* works on 10 randomly generated synchronous circuits.
        """
        for _ in range(10):
            g = gen_random_circuit()
            gr = opt1(g)
            self.assertLessEqual(cp(gr), cp(g))

    def test_random_opt2(self):
        """
        Check that *Algorithm OPT2* works on 10 randomly generated synchronous circuits.
        """
        for _ in range(10):
            g = gen_random_circuit()
            gr = opt2(g)
            self.assertLessEqual(cp(gr), cp(g))

    def test_already_minimum_graph(self):
        """
        Check that *Algorithms OPT1* and *OPT2* work on already minimum graphs.
        """
        g = nx.MultiDiGraph()
        add_weighted_node(g, 'h', 0)
        add_weighted_node(g, 'u', 2)
        add_weighted_node(g, 'v', 3)
        g.add_weighted_edges_from([('h', 'u', 0), ('u', 'v', 1), ('v', 'h', 1)])
        self.assertTrue(check_if_synchronous_circuit(g))
        gr = opt1(g)
        self.assertEqual(cp(gr), cp(g))
        gr = opt2(g)
        self.assertEqual(cp(gr), cp(g))
