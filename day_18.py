#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
from collections import namedtuple

test_input="""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

Cube = namedtuple("Cube", list("xyz"))

def cadd(c1, c2):
    return Cube(c1.x+c2.x, c1.y+c2.y, c1.z+c2.z)

# 6 directions
all_faces =     [Cube(1,0,0), Cube(-1,0,0), Cube(0,1,0), Cube(0,-1,0), Cube(0,0,1), Cube(0,0,-1)]
# inversions left/right up/down front/rear
all_faces_inv = {0:1, 1:0, 2:3, 3:2, 4:5, 5:4}
# hamming weight of the unsigned integers <= 0b111111
hamming_w =     [ 0, 1, 1, 2, 1, 2, 2, 3,
                  1, 2, 2, 3, 2, 3, 3, 4,
                  1, 2, 2, 3, 2, 3, 3, 4,
                  2, 3, 3, 4, 3, 4, 4, 5,
                  1, 2, 2, 3, 2, 3, 3, 4,
                  2, 3, 3, 4, 3, 4, 4, 5,
                  2, 3, 3, 4, 3, 4, 4, 5,
                  3, 4, 4, 5, 4, 5, 5, 6]

def parse_input(inputs):
    cubes = []
    re_int = re.compile("(-?[0-9]+)")
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers = [int(n) for n in re_int.findall(line)]
        cubes.append(Cube(*numbers))
    return cubes

def work_p1(inputs):
    cubes = parse_input(inputs)
    cubes = {c:0 for c in cubes}
    
    # for each cube, count the number of faces next to another block using a bitmask
    # each bit is for one face in all_faces
    for c1 in cubes:
        if cubes[c1] == 0b111111:
            continue
        for i in range(6):
            c2 = cadd(c1, all_faces[i])
            if c2 in cubes:
                cubes[c1] |= (1<<i)
                cubes[c2] |= (1<<all_faces_inv[i])
    
    # then use the hamming weight to count the number of free faces
    ret = sum(6-hamming_w[n] for c, n in cubes.items())
    return ret

def work_p2(inputs):   
    cubes = parse_input(inputs)
    
    # we will check all the cube in the enclosing range
    min_x = min(c.x for c in cubes)
    max_x = max(c.x for c in cubes)
    min_y = min(c.y for c in cubes)
    max_y = max(c.y for c in cubes)
    min_z = min(c.z for c in cubes)
    max_z = max(c.z for c in cubes)
    # create a color map with adjacent cubes
    colors = {}
    
    def in_range(c):
        return c.x >= min_x and c.x <= max_x and \
                c.y >= min_y and c.y <= max_y and \
                c.z >= min_z and c.z <= max_z
    
    to_check = set()
    for z in range(min_z, max_z + 1):
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                to_check.add(Cube(x,y,z))
    to_check -= set(cubes)

    outside_colors = set()   # reachable colors
    next_color = 0
    for cube in to_check:
        if cube in colors:
            continue
        stack = [cadd(cube, f) for f in all_faces]
        color = next_color
        next_color += 1
        colors[cube] = color
        while len(stack) != 0:
            c2 = stack.pop()
            if c2 in colors:
                continue
            if c2 in cubes:
                continue
            if in_range(c2):
                colors[c2] = color
                stack += [cadd(c2, f) for f in all_faces]
            else:
                outside_colors.add(color)
    
    # all the enclosed air cubes
    inner_space = {cube for cube, color in colors.items() if color not in outside_colors}
    # all cubes + inner cubes
    cubes = {c:0 for c in (set(cubes) | inner_space)}
    
    # same as part 1
    for c1 in cubes:
        if cubes[c1] == 0b111111:
            continue
        for i in range(6):
            c2 = cadd(c1, all_faces[i])
            if c2 in cubes:
                cubes[c1] |= (1<<i)
                cubes[c2] |= (1<<all_faces_inv[i])
    
    ret = sum(6-hamming_w[n] for c, n in cubes.items())
    return ret

def test_p1():
    assert(work_p1(["1,1,1", "2,1,1"]) == 10)
    assert(work_p1(test_input) == 64)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 58)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
