#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

test_input="""1
2
-3
3
-2
0
4
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

class Item(object):
    def __init__(self, v):
        self.v = v
    def __repr__(self):
        return repr(self.v)

def work_p1_p2(inputs, decryption_key=811589153, passes=10):
    numbers = [int(l.strip()) for l in inputs]
    numbers = [Item(n * decryption_key) for n in numbers]
    indexes = {numbers[i]:i for i in range(len(numbers))}
    N = len(numbers)

    for p in range(passes):
        for i in range(N):
            I = numbers[i]
            I_oidx = indexes[I]
            n = I.v
            I_nidx = (I_oidx + n) % (N-1)
            if I_nidx > I_oidx:
                for J, idx in indexes.items():
                    if I == J:
                        indexes[J] = I_nidx
                    elif idx > I_oidx and idx <= I_nidx:
                        indexes[J] -= 1
            elif I_nidx < I_oidx:
                for J, idx in indexes.items():
                    if I == J:
                        indexes[J] = I_nidx
                    elif idx < I_oidx and idx >= I_nidx:
                        indexes[J] += 1

    
    idx0 = None
    for I, idx in indexes.items():
        if I.v == 0:
            idx0 = idx
            break

    ret = 0
    for I, idx in indexes.items():
        if idx == ((idx0 + 1000) % N) or idx == ((idx0 + 2000) % N) or idx == ((idx0 + 3000) % N):
            ret += I.v
    return ret

def work_p2(inputs):
    pass

def test_p1():
    assert(work_p1_p2(test_input, 1, 1) == 3)
test_p1()

def p1():
    print(work_p1_p2(fileinput.input(), 1, 1))
p1()

def test_p2():
    assert(work_p1_p2(test_input) == 1623178306)
test_p2()

def p2():
    print(work_p1_p2(fileinput.input()))
p2()
