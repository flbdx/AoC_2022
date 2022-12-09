#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2

""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_09"]

def work(inputs, rope_len):
    moves = {'U': (0,1), 'D': (0,-1), 'L': (-1,0), 'R': (1, 0)}
    Tail_log = set()
    rope = list((0,0) for i in range(rope_len))
    
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        mv, steps = line.split(" ")
        steps = int(steps)
        mv = moves[mv]
        for i in range(steps):
            rope[0] = (rope[0][0] + mv[0], rope[0][1] + mv[1])
            
            for k in range(1, rope_len):
                if abs(rope[k-1][0] - rope[k][0]) <= 1 and abs(rope[k-1][1] - rope[k][1]) <= 1: # same or adjacent
                    pass
                else:
                    rope[k] = ( \
                        rope[k][0] + (1 if rope[k-1][0] > rope[k][0] else -1 if rope[k-1][0] < rope[k][0] else 0), \
                        rope[k][1] + (1 if rope[k-1][1] > rope[k][1] else -1 if rope[k-1][1] < rope[k][1] else 0))
                Tail_log.add(rope[-1])
    
    return len(Tail_log)

def work_p1(inputs):
    return work(inputs, 2)

def work_p2(inputs):
    return work(inputs, 10)

def test_p1():
    assert(work_p1(test_input) == 13)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 1)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
