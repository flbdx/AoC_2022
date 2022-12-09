#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""30373
25512
65332
33549
35390
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

def parse_input(inputs):
    trees = {}
    width = 0
    height = 0
    for y, line in enumerate(inputs):
        line = line.strip()
        height = max(height, y)
        if len(line) == 0:
            continue
        for x, c in enumerate(line):
            width = max(width, x)
            trees[(x,y)] = int(c)
    return trees, width+1, height+1

def work_p1(inputs):
    trees, width, height = parse_input(inputs)
    
    ret = 2 * width + 2*(height-2)
    visibles = set()
    
    for y in range(1, height - 1):
        for d in [-1, 1]:
            h = trees[(0 if d == 1 else (width - 1), y)]
            for x in range(1, width - 1) if d == 1 else range(width - 2, 0, -1):
                h2 = trees[(x,y)]
                if h2 > h:
                    visibles.add((x,y))
                    h = h2
                    if h == 9:
                        break
    
    for x in range(1, width - 1):
        for d in [-1, 1]:
            h = trees[(x, 0 if d == 1 else (height - 1))]
            for y in range(1, height - 1) if d == 1 else range(height - 2, 0, -1):
                h2 = trees[(x,y)]
                if h2 > h:
                    visibles.add((x,y))
                    h = h2
                    if h == 9:
                        break
    
    ret += len(visibles)
    return ret

def work_p2(inputs):
    trees, width, height = parse_input(inputs)
    
    def score(x, y):
        s = 1
        h = trees[(x,y)]
        for rng in [range(y-1, -1, -1), range(y+1, height)]:
            n = 0
            for y2 in rng:
                n += 1
                if trees[(x,y2)] >= h:
                    break
            s *= n
        for rng in [range(x-1, -1, -1), range(x+1, width)]:
            n = 0
            for x2 in rng:
                n += 1
                if trees[(x2,y)] >= h:
                    break
            s *= n
        return s
            
    
    ret = 0
    for x in range(width):
        for y in range(width):
            ret = max(ret, score(x,y))

    return ret

def test_p1():
    assert(work_p1(test_input) == 21)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 8)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
