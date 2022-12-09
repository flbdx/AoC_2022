#!/usr/bin/python3
#encoding: UTF-8

import sys

test_input="""1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

if len(sys.argv) == 1:
    sys.argv += ["input_01"]

test_input = test_input.strip()
real_input = open(sys.argv[1], encoding="UTF-8").read().strip()

def work_p1(s):
    return max([sum(map(int, l.split("\n"))) for l in s.split("\n\n")])

def work_p2(s):
    return sum(sorted([sum(map(int, l.split("\n"))) for l in s.split("\n\n")])[-3:])

def test_p1():
    assert(work_p1(test_input) == 24000)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 45000)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
