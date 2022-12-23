#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum

test_input="""....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".splitlines()

# test_input=""".....
# ..##.
# ..#..
# .....
# ..##.
# .....
# """.splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

class Direction(Enum):
    N = 0
    S = 1
    W = 2
    E = 3

    def adjacents(self, p):
        if self == Direction.N:
            return [(p[0] - 1, p[1] - 1), (p[0], p[1] - 1), (p[0] + 1, p[1] - 1)]
        if self == Direction.S:
            return [(p[0] - 1, p[1] + 1), (p[0], p[1] + 1), (p[0] + 1, p[1] + 1)]
        if self == Direction.W:
            return [(p[0] - 1, p[1] - 1), (p[0] - 1, p[1]), (p[0] - 1, p[1] + 1)]
        if self == Direction.E:
            return [(p[0] + 1, p[1] - 1), (p[0] + 1, p[1]), (p[0] + 1, p[1] + 1)]
    def next(self, p):
        if self == Direction.N:
            return (p[0], p[1] - 1)
        if self == Direction.S:
            return (p[0], p[1] + 1)
        if self == Direction.W:
            return (p[0] - 1, p[1])
        if self == Direction.E:
            return (p[0] + 1, p[1])

def all_adjacents(p):
    return [(p[0] + d[0], p[1] + d[1]) for d in ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))]


class Elf(object):
    def __init__(self, p):
        self.p = p
        self.d = Direction.N
        self.proposition = None
        self.did_move = None
    
    def propose(self, grid, propositions):
        all_empty = True
        for pt in all_adjacents(self.p):
            if pt in grid:
                all_empty = False
                break
        if all_empty:
            self.proposition = None
            return

        d = self.d
        for i in range(4):
            pts = d.adjacents(self.p)
            valid = True
            for pt in pts:
                if pt in grid:
                    valid = False
                    break
            if valid:
                pt = d.next(self.p)
                propositions[pt] = propositions.setdefault(pt, 0) + 1
                self.proposition = pt
                break
            d = Direction((d.value + 1) % 4)
    
    def move(self, propositions):
        if self.proposition != None:
            if propositions.get(self.proposition) == 1:
                self.p = self.proposition
                self.did_move = True
            else:
                self.did_move = False
            self.proposition = None
        else:
            self.did_move = False
        self.d = Direction((self.d.value + 1) % 4)

def parse_input(inputs):
    elves = []
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            continue
        for x, c in enumerate(line):
            if c == '#':
                elves.append(Elf((x, y)))
    return elves

def work_p1(inputs):
    elves = parse_input(inputs)
    grid = {elf.p for elf in elves}

    for i in range(10):
        propositions = {}
        for elf in elves:
            elf.propose(grid, propositions)
        for elf in elves:
            elf.move(propositions)
        grid = {elf.p for elf in elves}

    min_x = min(elf.p[0] for elf in elves)
    max_x = max(elf.p[0] for elf in elves)
    min_y = min(elf.p[1] for elf in elves)
    max_y = max(elf.p[1] for elf in elves)
    ret = (max_x - min_x + 1) * (max_y - min_y + 1) - len(grid)
    return ret
        
                

def work_p2(inputs):
    elves = parse_input(inputs)
    grid = {elf.p for elf in elves}

    round = 1
    while True:
        propositions = {}
        for elf in elves:
            elf.propose(grid, propositions)
        for elf in elves:
            elf.move(propositions)
        grid = {elf.p for elf in elves}
        tst = sum(1 for elf in elves if elf.did_move == False)
        if tst == len(elves):
            break
        round += 1
    return round

def test_p1():
    assert(work_p1(test_input) == 110)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 20)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
