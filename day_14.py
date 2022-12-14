#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import math
from enum import Enum

test_input="""498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_14"]

class Block(Enum):
    ROCK = "█"
    SAND = "o"
    AIR = "░"

def parse_input(inputs):
    grid = {}
    min_x, max_x, min_y, max_y = None, None, None, None
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        points = line.split(" -> ")
        points = [complex(*map(int, p.split(","))) for p in points]
        
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i+1]
            d = (p2 - p1)
            a =  math.sqrt(d.imag**2 + d.real**2)
            d = complex(d.real // a, d.imag // a)
            while p1 != p2 + d:
                grid[p1] = Block.ROCK
                min_x = int(p1.real if min_x == None or p1.real < min_x else min_x)
                max_x = int(p1.real if max_x == None or p1.real > max_x else max_x)
                min_y = int(p1.imag if min_y == None or p1.imag < min_y else min_y)
                max_y = int(p1.imag if max_y == None or p1.imag > max_y else max_y)
                
                p1 += d
        
    return (grid, min_x, max_x, min_y, max_y)

def work_p1(inputs):
    grid, min_x, max_x, min_y, max_y = parse_input(inputs)
        
    # for y in range(0, max_y + 1):
    #     line = ""
    #     for x in range(min_x, max_x + 1):
    #         line += grid.get(complex(x,y), Block.AIR).value
    #     print(line)
    # print("")
    
    drop_point = complex(500, 0)
    
    at_rest = True
    n_drop = 0
    while at_rest:
        p = complex(drop_point)
        n_drop += 1
        while True:
            if p.imag > max_y:
                at_rest = False
                break
            if grid.get(p + 1j, None) == None:
                p += 1j
            else:
                if grid.get(p + 1j - 1, None) == None:
                    p += 1j - 1
                else:
                    if grid.get(p + 1j + 1, None) == None:
                        p += 1j + 1
                    else:
                        break
        grid[p] = Block.SAND

    return n_drop - 1

def work_p2(inputs):
    grid, min_x, max_x, min_y, max_y = parse_input(inputs)
    floor_y = max_y + 2
    
    drop_point = complex(500, 0)
    
    n_drop = 0
    while True:
        p = complex(drop_point)
        if grid.get(p, None) != None:
            break
        n_drop += 1
        while True:
            if p.imag == floor_y - 1:
                break
            if grid.get(p + 1j, None) == None:
                p += 1j
            else:
                if grid.get(p + 1j - 1, None) == None:
                    p += 1j - 1
                else:
                    if grid.get(p + 1j + 1, None) == None:
                        p += 1j + 1
                    else:
                        break
        grid[p] = Block.SAND

    return n_drop

def test_p1():
    assert(work_p1(test_input) == 24)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 93)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
