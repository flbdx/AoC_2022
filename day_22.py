#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
import math

test_input="""        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_22"]

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def turn_right(self):
        return Direction((self.value + 1) % 4)
    def turn_left(self):
        return Direction((self.value - 1) % 4)

    def next(self, p):
        if self == Direction.UP:
            return (p[0], p[1] - 1)
        elif self == Direction.RIGHT:
            return (p[0] + 1, p[1])
        elif self == Direction.DOWN:
            return (p[0], p[1] + 1)
        else:
            return (p[0] - 1, p[1])

class Face(object):
    def __init__(self, fx, fy, width):
        self.fx = fx
        self.fy = fy
        self.width = width
        self.grid = {}
    def __repr__(self):
        return "Face " + repr((self.fx, self.fy))

class World(object):
    def __init__(self, inputs):
        self.grid = {}
        self.ranges_x = {}
        self.ranges_y = {}
        self.moves = []
        self.max_x = 0

        y = 1
        iter_line = iter(inputs)
        for line in iter_line:
            line = line.rstrip()
            if len(line) == 0:
                break
            self.ranges_x[y] = [1, 1]
            for x, c in enumerate(line, start=1):
                if c == ' ':
                    self.ranges_x[y][0] += 1
                else:
                    self.grid[(x,y)] = c
            self.ranges_x[y][1] = x
            self.max_x = max(self.max_x, x)
            y += 1
        self.max_y = y - 1

        self.cube_width = math.gcd(self.max_x, self.max_y)

        self.faces = {}
        for x, y in self.grid:
            fx, px = divmod(x-1, self.cube_width)
            fy, py = divmod(y-1, self.cube_width)
            face = self.faces.setdefault((fx,fy), Face(fx, fy, self.cube_width))
            face.grid[(px, py)] = self.grid[(x,y)]
        
        line = next(iter_line)
        b = ""
        for c in line:
            if c == 'R' or c == 'L':
                self.moves.append(int(b))
                self.moves.append(c)
                b = ""
            else:
                b += c
        if len(b) != 0:
            self.moves.append(int(b))

        current_face = None
        for fx, fy in self.faces:
            if fy == 0:
                if current_face == None or fx < current_face.fx:
                    current_face = self.faces[(fx, fy)]
        self.position = ((0,0),current_face)
        self.direction = Direction.RIGHT


    def advance(self, rules):
        p = self.position[0]
        face = self.position[1]
        next_p = self.direction.next(p)
        if not next_p in face.grid: # changement de face
            rule = rules[((face.fx, face.fy), self.direction)]
            if len(rule) == 3:
                next_face, next_dir, invert = rule
            else:
                next_face, next_dir = rule
                invert = False
            next_face = self.faces[next_face]
            if next_dir == self.direction:
                if next_dir == Direction.LEFT:
                    next_p = (self.cube_width - 1, p[1])
                elif next_dir == Direction.RIGHT:
                    next_p = (0, p[1])
                elif next_dir == Direction.UP:
                    next_p = (p[0], self.cube_width - 1)
                else:
                    next_p = (p[0], 0)
            elif (next_dir.value + 2) % 4 == self.direction.value: # direction opposée
                if next_dir == Direction.LEFT:
                    next_p = (self.cube_width - 1, self.cube_width - 1 - p[1])
                elif next_dir == Direction.RIGHT:
                    next_p = (0, self.cube_width - 1 - p[1])
                elif next_dir == Direction.UP:
                    next_p = (self.cube_width - 1 - p[0], self.cube_width - 1)
                else:
                    next_p = (self.cube_width - 1 - p[0], 0)
            else:
                if invert:
                    if next_dir == Direction.LEFT:
                        next_p = (self.cube_width - 1, self.cube_width - 1 - p[0])
                    elif next_dir == Direction.RIGHT:
                        next_p = (0, self.cube_width - 1 - p[0])
                    elif next_dir == Direction.UP:
                        next_p = (self.cube_width - 1 - p[1], self.cube_width - 1)
                    else:
                        next_p = (self.cube_width - 1 - p[1], 0)
                else:
                    if next_dir == Direction.LEFT:
                        next_p = (self.cube_width - 1, p[0])
                    elif next_dir == Direction.RIGHT:
                        next_p = (0, p[0])
                    elif next_dir == Direction.UP:
                        next_p = (p[1], self.cube_width - 1)
                    else:
                        next_p = (p[1], 0)
        else:
            next_face = face
            next_dir = self.direction
        if next_face.grid[next_p] == '#':
            next_p = p
            next_face = face
            next_dir = self.direction
        self.position = (next_p, next_face)
        self.direction = next_dir

    
    def turn_right(self):
        self.direction = self.direction.turn_right()
    def turn_left(self):
        self.direction = self.direction.turn_left()

    def do_moves(self, rules):
        for move in self.moves:
            if move == "R":
                self.turn_right()
                # print(move, self.position, self.direction)
            elif move == "L":
                self.turn_left()
                # print(move, self.position, self.direction)
            else:
                for i in range(move):
                    self.advance(rules)
                    # print(move, self.position, self.direction)

rules_test_p1 = {
    ((2,0), Direction.LEFT):    ((2,0), Direction.LEFT),
    ((2,0), Direction.RIGHT):   ((2,0), Direction.RIGHT),
    ((2,0), Direction.UP):      ((2,2), Direction.UP),
    ((2,0), Direction.DOWN):    ((2,1), Direction.DOWN),
    
    ((0,1), Direction.LEFT):    ((2,1), Direction.LEFT),
    ((0,1), Direction.RIGHT):   ((1,1), Direction.RIGHT),
    ((0,1), Direction.UP):      ((0,1), Direction.UP),
    ((0,1), Direction.DOWN):    ((0,1), Direction.DOWN),

    ((1,1), Direction.LEFT):    ((0,1), Direction.LEFT),
    ((1,1), Direction.RIGHT):   ((2,1), Direction.RIGHT),
    ((1,1), Direction.UP):      ((1,1), Direction.UP),
    ((1,1), Direction.DOWN):    ((1,1), Direction.DOWN),

    ((2,1), Direction.LEFT):    ((1,1), Direction.LEFT),
    ((2,1), Direction.RIGHT):   ((0,1), Direction.RIGHT),
    ((2,1), Direction.UP):      ((2,0), Direction.UP),
    ((2,1), Direction.DOWN):    ((2,2), Direction.DOWN),

    ((2,2), Direction.LEFT):    ((3,2), Direction.LEFT),
    ((2,2), Direction.RIGHT):   ((3,2), Direction.RIGHT),
    ((2,2), Direction.UP):      ((2,1), Direction.UP),
    ((2,2), Direction.DOWN):    ((2,0), Direction.DOWN),

    ((3,2), Direction.LEFT):    ((2,2), Direction.LEFT),
    ((3,2), Direction.RIGHT):   ((2,2), Direction.RIGHT),
    ((3,2), Direction.UP):      ((3,2), Direction.UP),
    ((3,2), Direction.DOWN):    ((3,2), Direction.DOWN)
}

rules_test_p2 = {
    ((2,0), Direction.LEFT):    ((1,1), Direction.DOWN),
    ((2,0), Direction.RIGHT):   ((3,2), Direction.LEFT),
    ((2,0), Direction.UP):      ((0,1), Direction.DOWN),
    ((2,0), Direction.DOWN):    ((2,1), Direction.DOWN),
    
    ((0,1), Direction.LEFT):    ((3,2), Direction.UP),
    ((0,1), Direction.RIGHT):   ((1,1), Direction.RIGHT),
    ((0,1), Direction.UP):      ((2,0), Direction.DOWN),
    ((0,1), Direction.DOWN):    ((2,2), Direction.UP),

    ((1,1), Direction.LEFT):    ((0,1), Direction.LEFT),
    ((1,1), Direction.RIGHT):   ((2,1), Direction.RIGHT),
    ((1,1), Direction.UP):      ((2,0), Direction.RIGHT),
    ((1,1), Direction.DOWN):    ((2,2), Direction.RIGHT, True),

    ((2,1), Direction.LEFT):    ((1,1), Direction.LEFT),
    ((2,1), Direction.RIGHT):   ((3,2), Direction.DOWN, True),
    ((2,1), Direction.UP):      ((2,0), Direction.UP),
    ((2,1), Direction.DOWN):    ((2,2), Direction.DOWN),

    ((2,2), Direction.LEFT):    ((1,1), Direction.UP, True),
    ((2,2), Direction.RIGHT):   ((3,2), Direction.RIGHT),
    ((2,2), Direction.UP):      ((2,1), Direction.UP),
    ((2,2), Direction.DOWN):    ((0,1), Direction.UP),

    ((3,2), Direction.LEFT):    ((2,2), Direction.LEFT),
    ((3,2), Direction.RIGHT):   ((2,0), Direction.LEFT),
    ((3,2), Direction.UP):      ((2,1), Direction.LEFT, True),
    ((3,2), Direction.DOWN):    ((0,1), Direction.RIGHT)
}

rules_p1 = {
    ((1,0), Direction.LEFT):    ((2,0), Direction.LEFT),
    ((1,0), Direction.RIGHT):   ((2,0), Direction.RIGHT),
    ((1,0), Direction.UP):      ((1,2), Direction.UP),
    ((1,0), Direction.DOWN):    ((1,1), Direction.DOWN),
    
    ((2,0), Direction.LEFT):    ((1,0), Direction.LEFT),
    ((2,0), Direction.RIGHT):   ((1,0), Direction.RIGHT),
    ((2,0), Direction.UP):      ((2,0), Direction.UP),
    ((2,0), Direction.DOWN):    ((2,0), Direction.DOWN),

    ((1,1), Direction.LEFT):    ((1,1), Direction.LEFT),
    ((1,1), Direction.RIGHT):   ((1,1), Direction.RIGHT),
    ((1,1), Direction.UP):      ((1,0), Direction.UP),
    ((1,1), Direction.DOWN):    ((1,2), Direction.DOWN),

    ((0,2), Direction.LEFT):    ((1,2), Direction.LEFT),
    ((0,2), Direction.RIGHT):   ((1,2), Direction.RIGHT),
    ((0,2), Direction.UP):      ((0,3), Direction.UP),
    ((0,2), Direction.DOWN):    ((0,3), Direction.DOWN),

    ((1,2), Direction.LEFT):    ((0,2), Direction.LEFT),
    ((1,2), Direction.RIGHT):   ((0,2), Direction.RIGHT),
    ((1,2), Direction.UP):      ((1,1), Direction.UP),
    ((1,2), Direction.DOWN):    ((1,0), Direction.DOWN),

    ((0,3), Direction.LEFT):    ((0,3), Direction.LEFT),
    ((0,3), Direction.RIGHT):   ((0,3), Direction.RIGHT),
    ((0,3), Direction.UP):      ((0,2), Direction.UP),
    ((0,3), Direction.DOWN):    ((0,2), Direction.DOWN)
}

rules_p2 = {
    ((1,0), Direction.LEFT):    ((0,2), Direction.RIGHT),
    ((1,0), Direction.RIGHT):   ((2,0), Direction.RIGHT),
    ((1,0), Direction.UP):      ((0,3), Direction.RIGHT),
    ((1,0), Direction.DOWN):    ((1,1), Direction.DOWN),
    
    ((2,0), Direction.LEFT):    ((1,0), Direction.LEFT),
    ((2,0), Direction.RIGHT):   ((1,2), Direction.LEFT),
    ((2,0), Direction.UP):      ((0,3), Direction.UP),
    ((2,0), Direction.DOWN):    ((1,1), Direction.LEFT),

    ((1,1), Direction.LEFT):    ((0,2), Direction.DOWN),
    ((1,1), Direction.RIGHT):   ((2,0), Direction.UP),
    ((1,1), Direction.UP):      ((1,0), Direction.UP),
    ((1,1), Direction.DOWN):    ((1,2), Direction.DOWN),

    ((0,2), Direction.LEFT):    ((1,0), Direction.RIGHT),
    ((0,2), Direction.RIGHT):   ((1,2), Direction.RIGHT),
    ((0,2), Direction.UP):      ((1,1), Direction.RIGHT),
    ((0,2), Direction.DOWN):    ((0,3), Direction.DOWN),

    ((1,2), Direction.LEFT):    ((0,2), Direction.LEFT),
    ((1,2), Direction.RIGHT):   ((2,0), Direction.LEFT),
    ((1,2), Direction.UP):      ((1,1), Direction.UP),
    ((1,2), Direction.DOWN):    ((0,3), Direction.LEFT),

    ((0,3), Direction.LEFT):    ((1,0), Direction.DOWN),
    ((0,3), Direction.RIGHT):   ((1,2), Direction.UP),
    ((0,3), Direction.UP):      ((0,2), Direction.UP),
    ((0,3), Direction.DOWN):    ((2,0), Direction.DOWN)
}

def work(inputs, test=False, part2 = False):
    world = World(inputs)
    if part2:
        if test:
            rules = rules_test_p2
        else:
            rules = rules_p2
    else:
        if test:
            rules = rules_test_p1
        else:
            rules = rules_p1
    world.do_moves(rules)
    pos, face = world.position
    px = world.cube_width * face.fx + pos[0] + 1
    py = world.cube_width * face.fy + pos[1] + 1
    ret = 1000 * py + 4 * px + world.direction.value
    return ret

def test_p1():
    assert(work(test_input, test=True) == 6032)
test_p1()

def p1():
    with fileinput.input() as inputs:
        print(work(inputs))
p1()

def test_p2():
    assert(work(test_input, test=True, part2=True) == 5031)
test_p2()

def p2():
    with fileinput.input() as inputs:
        print(work(inputs, test=False, part2=True))
p2()
