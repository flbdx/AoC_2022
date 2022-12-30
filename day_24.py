#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque, namedtuple
from enum import Enum
import math

test_input="""#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_24"]

def parse_input(inputs):
    blizzards_row = {}
    blizzards_col = {}
    grid = {}
    width = 0
    height = 0
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            continue
        for x, c in enumerate(line):
            grid[(x,y)] = c
        width = x + 1
        height = y + 1
    
    for p, v in grid.items():
        if v == '>':
            blizzards_row[p[1]] = blizzards_row.get(p[1], []) + [(p[0], 1)]
        elif v == '^':
            blizzards_col[p[0]] = blizzards_col.get(p[0], []) + [(p[1], -1)]
        elif v == '<':
            blizzards_row[p[1]] = blizzards_row.get(p[1], []) + [(p[0], -1)]
        elif v == 'v':
            blizzards_col[p[0]] = blizzards_col.get(p[0], []) + [(p[1], 1)]
    
    return (width, height, blizzards_col, blizzards_row)

class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def next(self, pt):
        return (pt[0] + self.value[0], pt[1] + self.value[1])

def work_p1_p2(inputs, part2 = False):
    width, height, blizzards_col, blizzards_row = parse_input(inputs)
    # print(width, height)
    starting_point = (1, 0)
    target_point = (width - 2, height - 1)

    def blizzard_at_point(pt, tstamp):
        for blz_p ,blz_d in blizzards_row.get(pt[1], []):
            p = blz_p - 1
            p += blz_d * tstamp
            p %= (width - 2)
            p += 1
            if p == pt[0]:
                return True
        for blz_p ,blz_d in blizzards_col.get(pt[0], []):
            p = blz_p - 1
            p += blz_d * tstamp
            p %= (height - 2)
            p += 1
            if p == pt[1]:
                return True
        return False
    
    period = math.lcm(width - 2, height - 2)
    State = namedtuple("State", ["pt", "tstamp"])

    best = 0

    def run():
        nonlocal best
        init_state = State(starting_point, best)
        stack = deque()
        stack.append(init_state)
        visited = set()
        visited.add((starting_point, best))

        best = None
        while len(stack) != 0:
            state = stack.popleft()
            if state.pt == target_point:
                if best == None or state.tstamp < best:
                    best = state.tstamp
                    print(state)
                continue
            if best != None and state.tstamp > best:
                continue
            for dir in [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]:
                next_pt = dir.next(state.pt)
                if next_pt[0] <= 0 or next_pt[0] >= (width - 1) or next_pt[1] <= 0 or next_pt[1] >= (height - 1):
                    if next_pt != starting_point and next_pt != target_point:
                        continue
                if not blizzard_at_point(next_pt, state.tstamp + 1):
                    sstate = (next_pt, (state.tstamp + 1) % period)
                    if not sstate in visited:
                        visited.add(sstate)
                        stack.append(State(next_pt, state.tstamp + 1))
            if not blizzard_at_point(state.pt, state.tstamp + 1):
                sstate = (state.pt, (state.tstamp + 1) % period)
                if not sstate in visited:
                    visited.add(sstate)
                    stack.append(State(state.pt, state.tstamp + 1))
    
    run()

    if part2:
        starting_point, target_point = target_point, starting_point
        run()
        starting_point, target_point = target_point, starting_point
        run()
        
    return best

def test_p1():
    assert(work_p1_p2(test_input) == 18)
test_p1()

def p1():
    print(work_p1_p2(fileinput.input()))
p1()

def test_p2():
    assert(work_p1_p2(test_input, True) == 54)
test_p2()

def p2():
    print(work_p1_p2(fileinput.input(), True))
p2()
