#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input=open("input_10_sample", "r", encoding="UTF-8").read().splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

def parse_input(inputs):
    instructions = []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        i = line.split()
        i = [i[0]] + list(map(int, i[1:]))
        instructions.append(i)
        # print(i)
    return instructions

latencies = {"addx": 2, "noop": 1}

class Cpu(object):
    def __init__(self, instructions):
        self.instructions = instructions
        self.ip = 0
        self.registers = {"x": 1}
        self.cycle = 0
        self.current = None
    
    def fetch_next_instruction(self):
        try:
            i = self.instructions[self.ip]
            self.ip += 1
            self.current = [latencies[i[0]], i[0], i[1:]]
        except:
            self.current == None
    
    def step(self):
        if self.current == None:
            self.fetch_next_instruction()
        else:
            self.current[0] -= 1
            self.cycle += 1
            if self.current[0] == 0:
                if self.current[1] == "addx":
                    self.registers['x'] += self.current[2][0]
                elif self.current[1] == "noop":
                    pass
                self.fetch_next_instruction()
    
    def n_steps(self, n):
        for i in range(n):
            self.step()
            

def work_p1(inputs):
    instructions = parse_input(inputs)
    cpu = Cpu(instructions)
    
    s = 0
    prev_steps = 0
    for steps in [20, 60, 100, 140, 180, 220]:
        cpu.n_steps(steps - prev_steps)
        prev_steps = steps
        s += cpu.registers['x'] * steps
    
    return s

def work_p2(inputs):
    instructions = parse_input(inputs)
    cpu = Cpu(instructions)
    
    display = {}
    width = 40
    height = 6
    
    ret = ""
    for y in range(0, height):
        for x in range(0, width):
            cpu.step()
            rx = cpu.registers['x']
            display[(x,y)] = '#' if x in [rx-1, rx, rx+1] else '.'
        ret += "".join(display[x,y] for x in range(0, width)) + "\n"
    return ret.strip("\n")
    

def test_p1():
    assert(work_p1(test_input) == 13140)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    ref="""##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
    assert(work_p2(test_input) == ref)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
