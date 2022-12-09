#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

test_input="""    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

class State(object):
    def __init__(self):
        self.stacks = []
    
    def read_stack_line(self, line):
        n_stacks = (len(line) + 1)//4
        if len(self.stacks) < n_stacks:
            self.stacks = [[] for s in range(n_stacks)]
        for s in range(n_stacks):
            c = line[1+4*s]
            if c == ' ':
                continue
            self.stacks[s].append(c) 

def work_p1(inputs):
    state = State()
    re_int = re.compile("[0-9]+")
    
    it = iter(inputs)
    while True:
        line = next(it)
        line = line.strip("\n\r")
        if "1" in line:
            break
        state.read_stack_line(line)
    next(it)

    try:
        while True:
            cmd = list(map(int, re_int.findall(next(it))))
            for i in range(cmd[0]):
                v = state.stacks[cmd[1] - 1].pop(0)
                state.stacks[cmd[2] - 1].insert(0, v)
    except StopIteration:
        return "".join(s[0] for s in state.stacks)

def work_p2(inputs):
    state = State()
    re_int = re.compile("[0-9]+")
    
    it = iter(inputs)
    while True:
        line = next(it)
        line = line.strip("\n\r")
        if "1" in line:
            break
        state.read_stack_line(line)
    next(it)

    try:
        while True:
            cmd = list(map(int, re_int.findall(next(it))))
            sub_stack = state.stacks[cmd[1] - 1][0:cmd[0]]
            state.stacks[cmd[1] - 1] = state.stacks[cmd[1] - 1][cmd[0]:]
            state.stacks[cmd[2] - 1] = sub_stack + state.stacks[cmd[2] - 1]
    except StopIteration:
        return "".join(s[0] for s in state.stacks)

def test_p1():
    assert(work_p1(test_input) == "CMZ")
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == "MCD")
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
