#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".splitlines()



if len(sys.argv) == 1:
    sys.argv += ["input_07"]

class Dir(object):
    def __init__(self, name):
        self.name = name
        self.entries = {}
        self.entries_keys = []
        self.sz = None
        
    def push(self, name, obj):
        self.entries[name] = obj
        self.entries_keys.append(name)
        
    def size(self):
        if self.sz == None:
            self.sz = sum([e.size() for e in self.entries.values()], 0)
        return self.sz

    def walk_dirs(self, func):
        stack = [e for e in self.entries.values() if type(e) == Dir]
        while len(stack) != 0:
            e = stack.pop()
            if type(e) == Dir:
                stack += [e for e in e.entries.values() if type(e) == Dir]
            func(e)

class File(object):
    def __init__(self, name, size):
        self.name = name
        self.sz = size
    def size(self):
        return self.sz

def parse_input(inputs):
    stack = []
    
    iter_line = iter(inputs)
    line = next(iter_line).strip()
    if line != "$ cd /":
        return None
    
    root = Dir("/")
    stack.append(root)
    
    for line in iter_line:
        line = line.strip()
        if len(line) == 0:
            continue
        if line == "$ ls":
            pass
        elif line[0] == "$":
            name = line[5:]
            if name == "..":
                stack.pop()
            else:
                stack.append(stack[-1].entries[name])
        else:
            p1, p2 = line.split(" ")
            if p1 == "dir":
                stack[-1].push(p2, Dir(p2))
            else:
                stack[-1].push(p2, File(p2, int(p1)))
    
    return root
                

def work_p1(inputs):
    root = parse_input(inputs)
    
    ret = 0
    def test(entry):
        nonlocal ret
        sz = entry.size()
        if sz <= 100000:
            ret += sz
    
    root.walk_dirs(test)
    return ret

def work_p2(inputs):
    root = parse_input(inputs)
    
    to_free = 30000000 - (70000000 - root.size())
    best_name = "/"
    best_sz = root.size()
    def test(entry):
        nonlocal best_name, best_sz, to_free
        sz = entry.size()
        if sz >= to_free and sz < best_sz:
            best_sz = sz
            best_name = entry.name

    root.walk_dirs(test)
    return best_sz

def test_p1():
    assert(work_p1(test_input) == 95437)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input) == 24933642)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
