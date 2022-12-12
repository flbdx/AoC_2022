#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import networkx as nx

test_input="""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_12"]

def parse_input(inputs):
    grid = {}
    start, end = None, None
    width, height = 0, 0
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        height = y + 1
        for x, c in enumerate(line):
            if c == 'S':
                start = complex(x,y)
                c = 'a'
            elif c == 'E':
                end = complex(x,y)
                c = 'z'
            grid[complex(x,y)] = ord(c) - ord('a')
        width = x + 1
    return grid, width, height, start, end

def build_graph(grid, width, height):
    dirs = [1, -1, 1j, -1j]

    G = nx.DiGraph()
    for y in range(height):
        for x in range(width):
            c = complex(x,y)
            v1 = grid[c]
            neighs = {d:grid.get(c + d, None) for d in dirs}
            for d, v2 in neighs.items():
                if v2 != None and v2 <= v1 + 1:
                    G.add_edge(c, c+d)
    return G

def work_p1(inputs):
    grid, width, height, start, end = parse_input(inputs)
    G = build_graph(grid, width, height)
    
    return nx.shortest_path_length(G, start, end)
                

def work_p2(inputs):
    grid, width, height, start, end = parse_input(inputs)
    G = build_graph(grid, width, height)
    
    best = None
    for y in range(height):
        for x in range(width):
            c = complex(x,y)
            if grid[c] == 0:
                try:
                    steps = nx.shortest_path_length(G, c, end)
                    if best == None or steps < best:
                        best = steps
                except nx.exception.NetworkXNoPath:
                    pass
    return best

def test_p1():
    assert(work_p1(test_input) == 31)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 29)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
