#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input=""">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_17"]

test_input = list(test_input[0].strip())
real_input = list(next(iter(fileinput.input())).strip())

class Rock(object):
    def __init__(self, number):
        self.number = number % 5
        if self.number == 0:
            self.shape = {(0,0), (1,0), (2,0), (3,0)}
            self.width = 4
            self.height = 1
            self.most_left = 0
            self.most_right = 3
        elif self.number == 1:
            self.shape = {       (1,2),\
                          (0,1), (1,1), (2,1),\
                                 (1,0)}
            self.width = 3
            self.height = 3
            self.most_left = 0
            self.most_right = 2
        elif self.number == 2:
            self.shape = {              (2,2),\
                                        (2,1),\
                          (0,0), (1,0), (2,0)}
            self.width = 3
            self.height = 3
            self.most_left = 0
            self.most_right = 2
        elif self.number == 3:
            self.shape = {(0,3),\
                          (0,2),\
                          (0,1),\
                          (0,0)}
            self.width = 1
            self.height = 4
            self.most_left = 0
            self.most_right = 0
        else:
            self.shape = {(0,1), (1,1),\
                          (0,0), (1,0)}
            self.width = 2
            self.height = 2
            self.most_left = 0
            self.most_right = 1

    def to_start_position(self, floor):
        self.shape = {(x+2, y+3+floor) for x,y in self.shape}
        self.most_left += 2
        self.most_right += 2
        
    def move_right(self):
        if self.most_right != 6:
            self.shape = {(x+1, y) for x,y in self.shape}
            self.most_left += 1
            self.most_right += 1
    def move_left(self):
        if self.most_left != 0:
            self.shape = {(x-1, y) for x,y in self.shape}
            self.most_left -= 1
            self.most_right -= 1
    def move_down(self):
        self.shape = {(x, y-1) for x,y in self.shape}
    def move_up(self):
        self.shape = {(x, y+1) for x,y in self.shape}

def work_p1(inputs):
    world = {(x,-1) for x in range(7)}
    floor = 0
    sequence = inputs
    sequence_n = 0
    for n in range(2022):
        p = Rock(n)
        p.to_start_position(floor)
        while True:
            d = sequence[sequence_n]
            sequence_n = (sequence_n + 1) % len(sequence)
            p.move_left() if d == '<' else p.move_right()
            if not world.isdisjoint(p.shape):
                p.move_right() if d == '<' else p.move_left()
            p.move_down()
            if not world.isdisjoint(p.shape):
                p.move_up()
                break
        world |= p.shape
        floor = max(floor, max(y + 1 for x,y in p.shape))
    
    return floor
            

def work_p2(inputs):
    sequence = inputs    
    record = {}
    world = {(x,-1) for x in range(7)}
    floor = 0
    sequence_n = 0
    n = 0
    while True:
        p = Rock(n)
        p.to_start_position(floor)
        while True:
            d = sequence[sequence_n % len(sequence)]
            sequence_n += 1
            p.move_left() if d == '<' else p.move_right()
            if not world.isdisjoint(p.shape):
                p.move_right() if d == '<' else p.move_left()
            p.move_down()
            if not world.isdisjoint(p.shape):
                p.move_up()
                break
        world |= p.shape
        floor = max(floor, max(y + 1 for x,y in p.shape))
        
        record_line  = "".join('#' if (x,floor) in world else '.' for x in range(7))
        record_line += "".join('#' if (x,floor-1) in world else '.' for x in range(7))
        
        # cycle detection by recording the last 2 floors
        record[record_line] = record.setdefault(record_line, []) + [(sequence_n % len(sequence), n%5, floor, n)]
        if len(record[record_line]) > 1:
            r = record[record_line]
            # check same wind sequence and piece sequence
            if len({(t[0], t[1]) for t in r}) == 1:
                # check same floor diff
                if len({r[i+1][2] - r[i][2] for i in range(len(r)-1)}) == 1:
                    # check same lenght
                    if len({r[i+1][3] - r[i][3] for i in range(len(r)-1)}) == 1:
                        cycle_len = r[-1][3] - r[-2][3]
                        cycle_start = r[-1][3]
                        cycle_floor_start = r[-2][2]
                        cycle_floor_height = r[-1][2] - r[-2][2]
                        break
        n += 1
    del record
    
    target = 1000000000000
    result = cycle_floor_start
    target -= cycle_start
    n_cycles, rem = divmod(target, cycle_len)
    result += n_cycles * cycle_floor_height
    
    world = {(x,-1) for x in range(7)}
    floor = 0
    sequence_n = 0
    for n in range(cycle_start + rem):
        p = Rock(n)
        p.to_start_position(floor)
        while True:
            d = sequence[sequence_n]
            sequence_n = (sequence_n + 1) % len(sequence)
            p.move_left() if d == '<' else p.move_right()
            if not world.isdisjoint(p.shape):
                p.move_right() if d == '<' else p.move_left()
            p.move_down()
            if not world.isdisjoint(p.shape):
                p.move_up()
                break
        world |= p.shape
        floor = max(floor, max(y + 1 for x,y in p.shape))
        
    result = result + floor - cycle_floor_start
    return result
        
    
def test_p1():
    assert(work_p1(test_input) == 3068)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 1514285714288)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
