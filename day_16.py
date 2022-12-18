#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
import networkx as nx
from collections import namedtuple, deque
from itertools import combinations, permutations

test_input="""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_16"]

def parse_input(inputs):
    re_line = re.compile("^Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([, A-Z]+)$")
    valves = {}
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        m = re_line.fullmatch(line).groups()
        valve = m[0]
        rate = int(m[1])
        connected = m[2].split(", ")
        valves[valve] = (valve, rate, connected)
    return valves

def work_p1(inputs):
    valves = parse_input(inputs)
    
    productive_valves = [v for v in valves.values() if v[1] != 0]
    
    distances = {}
    
    # this graph is used to precompute the distance between the productive nodes
    # and the distances starting from AA
    G = nx.Graph()
    for v in valves.values():
        for v2 in v[2]:
            G.add_edge(v[0], v2)
    
    for i in range(len(productive_valves)):
        v1 = productive_valves[i][0]
        d = nx.shortest_path_length(G, 'AA', v1)
        distances['AA'] = distances.setdefault('AA', {}) | {v1:d}
        for j in range(i+1, len(productive_valves)):
            v2 = productive_valves[j][0]
            d = nx.shortest_path_length(G, v1, v2)
            distances[v1] = distances.setdefault(v1, {}) | {v2:d}
            distances[v2] = distances.setdefault(v2, {}) | {v1:d}
    
    State = namedtuple("State", ["valve", "score", "to_visit", "rem"])
    stack = [State("AA", 0, [v[0] for v in productive_valves], 30)]
    best = 0
    while len(stack) != 0:
        state = stack.pop(0)
        v1 = state.valve
        score = state.score
        if score > best:
            best = score
        for i in range(len(state.to_visit)):
            v2 = state.to_visit[i]
            d = distances[v1][v2]
            if d + 1 >= state.rem:
                continue
            gain = (state.rem - d - 1) * valves[v2][1]
            stack.append(State(v2, score + gain, state.to_visit[0:i] + state.to_visit[i+1:], state.rem - d - 1))
    return best

def work_p2(inputs):
    valves = parse_input(inputs)
    
    productive_valves = [v for v in valves.values() if v[1] != 0]
    
    distances = {}
    
    # this graph is used to precompute the distance between the productive nodes
    # and the distances starting from AA
    G = nx.Graph()
    for v in valves.values():
        for v2 in v[2]:
            G.add_edge(v[0], v2)
    
    for i in range(len(productive_valves)):
        v1 = productive_valves[i][0]
        d = nx.shortest_path_length(G, 'AA', v1)
        distances['AA'] = distances.setdefault('AA', {}) | {v1:d}
        for j in range(i+1, len(productive_valves)):
            v2 = productive_valves[j][0]
            d = nx.shortest_path_length(G, v1, v2)
            distances[v1] = distances.setdefault(v1, {}) | {v2:d}
            distances[v2] = distances.setdefault(v2, {}) | {v1:d}
    
    # associate one bit to each productive valve, to build a bitmask of the visited valves
    bits = {}
    for i in range(len(productive_valves)):
        bits[productive_valves[i][0]] = 1 << (i + 1)
    
    State = namedtuple("State", ["valve", "score", "to_visit", "rem", "mask"])
    stack = [State("AA", 0, [v[0] for v in productive_valves], 26, 0)]
    bests = {}      # store the best score for a given bitmask
    while len(stack) != 0:
        state = stack.pop(0)
        v1 = state.valve
        score = state.score
        if score > bests.get(state.mask, 0):
            bests[state.mask] = score
        for i in range(len(state.to_visit)):
            v2 = state.to_visit[i]
            d = distances[v1][v2]
            if d + 1 >= state.rem:
                continue
            gain = (state.rem - d - 1) * valves[v2][1]
            stack.append(State(v2, score + gain, state.to_visit[0:i] + state.to_visit[i+1:], state.rem - d - 1, state.mask + bits[v2]))
    
    # find the best 2 disjoint paths using the bitmasks!
    ret = 0
    for k1, s1 in bests.items():
        for k2, s2 in bests.items():
            if (k1 & k2) == 0 and (s1 + s2) > ret:
                ret = s1 + s2
    return ret
            

def test_p1():
    assert(work_p1(test_input) == 1651)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 1707)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
