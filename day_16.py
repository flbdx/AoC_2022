#!/usr/bin/python3
#encoding: UTF-8

# part 2 will take a few hours...

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
    
    # for v2, d in distances['AA'].items():
        # print(v2, d, (30-d - 1)*valves[v2][1])
    
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
    
    # objectives: list of nodes to visit, (node, distance)
    #             the distance includes +1 to open the valve
    # flow: flow of the opened valves
    # score: deplaced volume
    # to_visit: set of productives valves yet to visit
    # rem: time remaining
    State = namedtuple("State", ["objectives", "flow", "score", "to_visit", "rem"])
    pv = set(v[0] for v in productive_valves)
    stack = deque()
    for nv1, nv2 in combinations(pv, 2):
        d1, d2 = distances["AA"][nv1] + 1, distances["AA"][nv2] + 1
        if d1 <= 26 and d2 <= 26:
            stack.append(State([(nv1, d1), (nv2, d2)], 0, 0, pv - {nv1, nv2}, 26))
    
    best = 0
    while len(stack) != 0:
        state = stack.pop()
        
        # number of minutes to simulate
        delta = state.rem
        if len(state.objectives) != 0:
            delta = min(o[1] for o in state.objectives)
        if delta > state.rem:
            delta = state.rem
        rem = state.rem - delta
        
        score = state.score
        flow = state.flow
        score += flow * delta
        
        if rem == 0:
            if score > best:
                print(score, state)
                best = score
            continue
        
        nobjs = []
        starting_points = []
        for o in state.objectives:
            if o[1] != delta:
                nobjs.append((o[0], o[1] - delta))
            else:
                flow += valves[o[0]][1]
                starting_points.append(o[0])
        
        to_fill = 2 - len(nobjs)
                
        if len(state.to_visit) == 0:
            stack.append(State(nobjs, flow, score, state.to_visit, rem))
        else:
            if to_fill == 2 and len(state.to_visit) >= 2:
                for nv1, nv2 in combinations(state.to_visit, 2):
                    nobjs1 = [(nv1, distances[starting_points[0]][nv1] + 1), (nv2, distances[starting_points[1]][nv2] + 1)]
                    stack.append(State(nobjs1, flow, score, state.to_visit - {nv1, nv2}, rem))
                    nobjs2 = [(nv2, distances[starting_points[0]][nv2] + 1), (nv1, distances[starting_points[1]][nv1] + 1)]
                    stack.append(State(nobjs2, flow, score, state.to_visit - {nv1, nv2}, rem))
            elif to_fill == 2 and len(state.to_visit) == 1:
                for nv in state.to_visit:
                    nobjs1 = nobjs + [(nv, distances[starting_points[0]][nv] + 1)]
                    stack.append(State(nobjs1, flow, score, state.to_visit - {nv}, rem))
                    nobjs2 = nobjs + [(nv, distances[starting_points[1]][nv] + 1)]
                    stack.append(State(nobjs2, flow, score, state.to_visit - {nv}, rem))
            elif to_fill == 1:
                for nv in state.to_visit:
                    nobjs_ = nobjs + [(nv, distances[starting_points[0]][nv] + 1)]
                    stack.append(State(nobjs_, flow, score, state.to_visit - {nv}, rem))
            elif to_fill == 0:
                stack.append(State(nobjs, flow, score, state.to_visit, rem))

                    

    return best
            

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
# p2()
