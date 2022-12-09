#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

def type_to_value(c):
    return ord(c) + ((1 - ord('a')) if c.islower() else (27 - ord('A')))

def work_p1(inputs):
    ret = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        cs1 = set(map(type_to_value, line[:len(line)//2]))
        cs2 = set(map(type_to_value, line[len(line)//2:]))
        ret += cs1.intersection(cs2).pop()
    return ret

def work_p2(inputs):
    ret = 0
    it = iter(inputs)
    while True:
        try:
            s1 = set(map(type_to_value, next(it).strip()))
            s2 = set(map(type_to_value, next(it).strip()))
            s3 = set(map(type_to_value, next(it).strip()))
            ret += s1.intersection(s2).intersection(s3).pop()
        except:
            break
    return ret

def test_p1():
    assert(work_p1(test_input) == 157)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 70)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
