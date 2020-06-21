#!/usr/bin/env python3

from unittest import TestCase

from algos import cp
from gutils import load_graph


class Tests(TestCase):

    def test_correlator1_cp(self):
        g = load_graph('../graphs/correlator1.dot')
        clock_period = cp(g)
        self.assertEqual(clock_period, 24)

    def test_correlator2_cp(self):
        g = load_graph('../graphs/correlator2.dot')
        clock_period = cp(g)
        self.assertEqual(clock_period, 17)
