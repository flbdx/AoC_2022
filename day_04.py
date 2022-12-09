#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

def spans_contain(s1, s2): # returns True if one span contains the other
    return (s2[0] >= s1[0] and s2[1] <= s1[1]) or (s1[0] >= s2[0] and s1[1] <= s2[1])

def spans_overlap(s1, s2): # returns True if the 2 spans overlap
    return (s2[0] >= s1[0] and s2[0] <= s1[1]) or (s1[0] >= s2[0] and s1[0] <= s2[1])

def work_p1_p2(inputs, test):
    ret = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        s1, s2 = [tuple(map(int, s.split("-"))) for s in line.split(",")]
        if test(s1, s2):
            ret += 1
    return ret

def test_p1():
    assert(work_p1_p2(test_input, spans_contain) == 2)
test_p1()

def p1():
    print(work_p1_p2(fileinput.input(), spans_contain))
p1()

def test_p2():
    assert(work_p1_p2(test_input, spans_overlap) == 4)
test_p2()

def p2():
    print(work_p1_p2(fileinput.input(), spans_overlap))
p2()
