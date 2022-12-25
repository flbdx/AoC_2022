#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""1=-0-2
 12111
  2=0=
    21
  2=01
   111
 20012
   112
 1=-1=
  1-12
    12
    1=
   122
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_25"]

def snafu_decode(number):
    base = 1
    n = 0
    table = {
        '=': -2,
        '-': -1,
        '0': 0,
        '1': 1,
        '2' : 2
    }
    for c in reversed(number):
        n += base * table[c]
        base *= 5
    return n

def snafu_encode(number):
    ret = ""
    base = 1
    table = {-2:'=', -1:'-', 0:'0', 1:'1', 2:'2'}
    while number != 0:
        q, r = divmod(number, 5)
        if r >= 3:
            r = r - 5
            q += 1
        ret = table[r] + ret
        number = q
    return ret

def work_p1(inputs):
    total = 0
    for line in inputs:
        line = line.strip()
        total += snafu_decode(line)
    return snafu_encode(total)

def test_p1():
    assert(work_p1(test_input) == "2=-1=0")
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()
