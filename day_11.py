#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
import math

test_input=open("input_11_sample", "r", encoding="UTF-8").read().splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

class Monkey(object):
    def __init__(self, items, op, test, test_n):
        self.items = items
        self.op = op
        self.test = test
        self.test_n = test_n
        self.inspected = 0
    
    def round_p1(self):
        result = []
        for item in self.items:
            w = self.op(item) // 3
            self.inspected += 1
            result.append((w, self.test(w)))
        self.items = []
        return result
    
    def round_p2(self, mod):
        result = []
        for item in self.items:
            w = self.op(item) % mod
            self.inspected += 1
            result.append((w, self.test(w)))
        self.items = []
        return result

    def add_item(self, item):
        self.items.append(item)

def parse_inputs(inputs):
    monkeys = {}
    it = iter(inputs)
    re_int = re.compile("([-]?[0-9]+)")
    re_op = re.compile(".*new = old ([*+]) ([0-9]+|old)")
    
    try:
        while True:
            monkey_n = int(re_int.findall(next(it).strip())[0])
            starting_items = list(map(int, re_int.findall(next(it).strip())))
            ope_match = re_op.match(next(it).strip())
            div_test = int(re_int.findall(next(it).strip())[0])
            send_true = int(re_int.findall(next(it).strip())[0])
            send_false = int(re_int.findall(next(it).strip())[0])
            
            if ope_match.group(1) == '*':
                if ope_match.group(2).isdecimal():
                    op = lambda x,n=int(ope_match.group(2)) : x * n
                else:
                    op = lambda x : x * x
            else:
                if ope_match.group(2).isdecimal():
                    op = lambda x,n=int(ope_match.group(2)) : x + n
                else:
                    op = lambda x : x + x
            
            test = lambda x,st=send_true, sf=send_false, d=div_test : st if ((x%d) == 0) else sf
            
            monkeys[monkey_n] = Monkey(starting_items, op, test, div_test)
            
            next(it)
    except:
        return monkeys

def work_p1(inputs):
    monkeys = parse_inputs(inputs)
    
    for rnd in range(20):
        for monkey in monkeys.values():
            for w, n in monkey.round_p1():
                monkeys[n].add_item(w)
    
    activities = sorted(m.inspected for m in monkeys.values())
    return activities[-1] * activities[-2]

def work_p2(inputs):
    monkeys = parse_inputs(inputs)
    worry_mod = math.lcm(*[m.test_n for m in monkeys.values()])
    
    for rnd in range(10000):
        for monkey in monkeys.values():
            for w, n in monkey.round_p2(worry_mod):
                monkeys[n].add_item(w)
    
    activities = sorted(m.inspected for m in monkeys.values())
    return activities[-1] * activities[-2]

def test_p1():
    assert(work_p1(test_input) == 10605)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 2713310158)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
