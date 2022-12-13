#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import ast

test_input="""[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]

""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_13"]
    
def read_input(inputs):
    out = []
    it = iter(inputs)
    try:
        while True:
            l1 = ast.literal_eval(next(it).strip())
            l2 = ast.literal_eval(next(it).strip())
            out.append((l1, l2))
            next(it)
    except:
        return out

def compare(p1, p2):
    if type(p1) == int and type(p2) == int:
        return -1 if p1 < p2 else 1 if p1 > p2 else 0
    
    if type(p1) == list and type(p2) == list:
        l1, l2 = len(p1), len(p2)
        for i in range(min(l1, l2)):
            r = compare(p1[i], p2[i])
            if r == 1 or r == -1:
                return r
        return -1 if l1 < l2 else 1 if l2 < l1 else 0
    
    if type(p1) == int:
        p1 = [p1]
    if type(p2) == int:
        p2 = [p2]
    return compare(p1, p2)

class Paquet(object):
    def __init__(self, p):
        self.p = p
    def __lt__(self, o):
        return compare(self.p, o.p) < 0
    def __eq__(self, o):
        return self.p == o.p

def work_p1(inputs):
    pairs = read_input(inputs)
    
    res = 0
    i = 0
    for p in pairs:
        i += 1
        if compare(p[0], p[1]) < 0:
            res += i
    return res

def work_p2(inputs):
    pairs = read_input(inputs)
    packets = sum((list(p) for p in pairs), [])
    packets.append([[2]])
    packets.append([[6]])
    
    res = 1
    i = 0
    for p in sorted(packets, key=lambda p: Paquet(p)):
        i += 1
        if p == [[2]] or p == [[6]]:
            res *= i
    return res

def test_p1():
    assert(work_p1(test_input) == 13)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 140)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
