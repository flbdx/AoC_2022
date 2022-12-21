#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

class Node(object):
    def __init__(self, name):
        self.name = name
    
class LeafNode(Node):
    def __init__(self, name, value):
        super(LeafNode, self).__init__(name)
        self.value = value
    def v(self):
        return self.value

class OpeNode(Node):
    def __init__(self, name, ope, nodel, noder, opename):
        super(OpeNode, self).__init__(name)
        self.ope = ope
        self.nodel = nodel
        self.noder = noder
        self.opename = opename
        self.cache = None
    def v(self):
        if self.cache != None:
            return self.cache
        self.cache = self.ope(self.nodel, self.noder)
        return self.cache
    
    def expected(self, all_nodes, parent_value):
        try:
            vleft = all_nodes[self.nodel].v()
        except:
            vleft = None
        try:
            vright = all_nodes[self.noder].v()
        except:
            vright = None
        if self.opename == "=":
            return ("left", vright) if vleft == None else ("right", vleft)
        if self.opename == "/":
            return ("left", parent_value * vright) if vleft == None else ("right", vleft // parent_value)
        if self.opename == "*":
            return ("left", parent_value // vright) if vleft == None else ("right", parent_value // vleft)
        if self.opename == "+":
            return ("left", parent_value - vright) if vleft == None else ("right", parent_value - vleft)
        if self.opename == "-":
            return ("left", parent_value + vright) if vleft == None else ("right", vleft - parent_value)

def parse_input(inputs):
    all_nodes = {}
    operators = {"*": lambda x,y:x*y,\
                 "/": lambda x,y:x//y,\
                 "+": lambda x,y:x+y,\
                 "-": lambda x,y:x-y,\
                 "=": lambda x,y:x==y}
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        name, value = line.split(": ")
        if value.isnumeric():
            all_nodes[name] = LeafNode(name, int(value))
        else:
            n1, operator, n2 = value.split(" ")
            ope = lambda name1, name2, f=operators[operator]: f(all_nodes[name1].v(), all_nodes[name2].v())
            all_nodes[name] = OpeNode(name, ope, n1, n2, operator)
    
    return all_nodes

def work_p1(inputs):
    all_nodes = parse_input(inputs)
    root_node = all_nodes["root"]
    return root_node.v()

def work_p2(inputs):
    all_nodes = parse_input(inputs)
    root_node = all_nodes["root"]
    root_node.ope = lambda name1, name2: all_nodes[name1].v() == all_nodes[name2].v()
    root_node.opename = "="
    all_nodes["humn"].value = None

    cur_name = "root"
    parent_value = None
    while True:
        direction, value = all_nodes[cur_name].expected(all_nodes, parent_value)
        cur_name = all_nodes[cur_name].nodel if direction == "left" else all_nodes[cur_name].noder
        parent_value = value
        if cur_name == "humn":
            break
    return parent_value

def test_p1():
    assert(work_p1(test_input) == 152)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 301)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
