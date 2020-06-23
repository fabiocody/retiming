#!/usr/bin/env python3

from utils import load_graph, draw_graph
from algos import opt1, opt2, cp


if __name__ == '__main__':
    g = load_graph('../graphs/correlator1.dot')
    draw_graph(g)
    gr1 = opt1(g)
    draw_graph(gr1)
    gr2 = opt2(g)
    draw_graph(gr2)
    assert cp(gr1) == cp(gr2)
