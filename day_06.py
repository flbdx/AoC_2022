#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_06"]

def is_marker(seq, p):
    s = { *seq[p:p+4] }
    return len(s) == 4

def is_msg(seq, p):
    s = { *seq[p:p+14] }
    return len(s) == 14

def work_p1(inputs):
    line = next(iter(inputs)).strip()
    
    ret = 0
    try:
        while True:
            if is_marker(line, ret):
                return ret + 4
            ret += 1
    except:
        return None

def work_p2(inputs):
    line = next(iter(inputs)).strip()
    
    ret = 0
    try:
        while True:
            if is_msg(line, ret):
                return ret + 14
            ret += 1
    except:
        return None
    
def test_p1():
    assert(work_p1(test_input) == 11)
test_p1()

def p1():
    with fileinput.input() as inputs:
        print(work_p1(inputs))
p1()

def test_p2():
    assert(work_p2(test_input) == 26)
test_p2()

def p2():
    with fileinput.input() as inputs:
        print(work_p2(inputs))
p2()
