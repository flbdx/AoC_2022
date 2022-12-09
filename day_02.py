#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""A Y
B X
C Z
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_02"]

def work_p1(inputs):
    syms = {"A":0, "B":1, "C":2, "X":0, "Y":1, "Z":2}
    
    score = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        elf, me = [syms[v] for v in line.split(" ")]
        outcome = (me - elf + 1) % 3
        score += outcome * 3 + me + 1
        
    return score

def work_p2(inputs):
    syms = {"A":0, "B":1, "C":2, "X":-1, "Y":0, "Z":1}
    
    score = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        elf, to_play = [syms[v] for v in line.split(" ")]
        me = (elf + to_play) % 3 
        score += (to_play + 1) * 3 + me + 1
    return score

def test_p1():
    assert(work_p1(test_input) == 15)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 12)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
