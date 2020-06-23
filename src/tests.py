#!/usr/bin/env python3

from unittest import TestCase
import numpy as np
from algos import cp, wd, retime, opt1, feas, opt2
from utils import load_graph, wd2numpy


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
        W = wd2numpy(W)
        D = wd2numpy(D)
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
