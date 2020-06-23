#!/usr/bin/env python3

from unittest import TestCase
import numpy as np
from algos import cp, wd, retime, opt1, feas, opt2
from structures import MyTuple
from utils import load_graph, check_if_synchronous_circuit, gen_random_circuit


def wd2numpy_correlator(m):
    order = ['h', 'd0', 'd1', 'd2', 'd3', 'p2', 'p1', 'p0']
    lists = [[] for _ in order]
    for u in order:
        for v in order:
            lists[order.index(u)].append(m[u][v])
    return np.array(lists)


class Tests(TestCase):

    def test_correlator1_cp(self):
        g = load_graph('../graphs/correlator1.dot')
        clock_period = cp(g)
        self.assertEqual(clock_period, 24)

    def test_correlator2_cp(self):
        g = load_graph('../graphs/correlator2.dot')
        clock_period = cp(g)
        self.assertEqual(clock_period, 17)

    def test_correlator1_wd(self):
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
        g = load_graph('../graphs/correlator1.dot')
        gr = opt1(g)
        self.assertEqual(cp(gr), 13)

    def test_correlator2_opt1(self):
        g = load_graph('../graphs/correlator2.dot')
        gr = opt1(g)
        self.assertEqual(cp(gr), 13)

    def test_correlator1_feas(self):
        g = load_graph('../graphs/correlator1.dot')
        r = feas(g, 13)
        self.assertIsNotNone(r)
        gr = retime(g, r)
        self.assertEqual(cp(gr), 13)

    def test_correlator2_feas(self):
        g = load_graph('../graphs/correlator2.dot')
        r = feas(g, 13)
        self.assertIsNotNone(r)
        gr = retime(g, r)
        self.assertEqual(cp(gr), 13)

    def test_correlator1_opt2(self):
        g = load_graph('../graphs/correlator1.dot')
        gr = opt2(g)
        self.assertEqual(cp(gr), 13)

    def test_correlator2_opt2(self):
        g = load_graph('../graphs/correlator2.dot')
        gr = opt2(g)
        self.assertEqual(cp(gr), 13)

    def test_MyTuple(self):
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
        g = load_graph('../graphs/correlator1.dot')
        self.assertTrue(check_if_synchronous_circuit(g))
        gr = opt2(g)
        self.assertTrue(check_if_synchronous_circuit(gr))

    def test_correlator2_synchronous_circuit(self):
        g = load_graph('../graphs/correlator2.dot')
        self.assertTrue(check_if_synchronous_circuit(g))
        gr = opt2(g)
        self.assertTrue(check_if_synchronous_circuit(gr))

    '''def test_random_opt1(self):
        for _ in range(100):
            g = gen_random_circuit(N=8, E=11)
            gr = opt1(g)
            self.assertLessEqual(cp(gr), cp(g))

    def test_random_opt2(self):
        for _ in range(100):
            g = gen_random_circuit(N=8, E=11)
            gr = opt2(g)
            self.assertLessEqual(cp(gr), cp(g))'''
