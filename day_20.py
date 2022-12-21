#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

test_input="""1
2
-3
3
-2
0
4
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

class Item(object):
    def __init__(self, v):
        self.v = v
    def __repr__(self):
        return repr(self.v)

def work_p1_p2(inputs, decryption_key=811589153, passes=10):
    numbers = [int(l.strip()) for l in inputs]
    numbers = [Item(n * decryption_key) for n in numbers]
    indexes = {numbers[i]:i for i in range(len(numbers))}
    N = len(numbers)

    for p in range(passes):
        for i in range(N):
            I = numbers[i]
            I_oidx = indexes[I]
            n = I.v
            I_nidx = (I_oidx + n) % (N-1)
            if I_nidx > I_oidx:
                for J, idx in indexes.items():
                    if I == J:
                        indexes[J] = I_nidx
                    elif idx > I_oidx and idx <= I_nidx:
                        indexes[J] -= 1
            elif I_nidx < I_oidx:
                for J, idx in indexes.items():
                    if I == J:
                        indexes[J] = I_nidx
                    elif idx < I_oidx and idx >= I_nidx:
                        indexes[J] += 1



        # print(sorted(indexes, key=lambda x: indexes[x]), indexes)
    
    idx0 = None
    for I, idx in indexes.items():
        if I.v == 0:
            idx0 = idx
            break

    ret = 0
    for I, idx in indexes.items():
        if idx == ((idx0 + 1000) % N) or idx == ((idx0 + 2000) % N) or idx == ((idx0 + 3000) % N):
            # print(I.v)
            ret += I.v
    return ret

    # numbers = [int(l.strip()) for l in inputs]
    # numbers = [Item(n) for n in numbers]
    # indexes = {numbers[i]:i for i in range(len(numbers))}
    # N = len(numbers)

    # for i in range(N):
    #     I = numbers[i]
    #     I_oidx = indexes[I]
    #     n = I.v
    #     I_nidx = (I_oidx + n) % (N-1)
    #     if I_nidx > I_oidx:
    #         for J, idx in indexes.items():
    #             if I == J:
    #                 indexes[J] = I_nidx
    #             elif idx > I_oidx and idx <= I_nidx:
    #                 indexes[J] -= 1
    #     elif I_nidx < I_oidx:
    #         for J, idx in indexes.items():
    #             if I == J:
    #                 indexes[J] = I_nidx
    #             elif idx < I_oidx and idx >= I_nidx:
    #                 indexes[J] += 1



    #     # print(sorted(indexes, key=lambda x: indexes[x]), indexes)
    
    # idx0 = None
    # for I, idx in indexes.items():
    #     if I.v == 0:
    #         idx0 = idx
    #         break

    # ret = 0
    # for I, idx in indexes.items():
    #     if idx == ((idx0 + 1000) % N) or idx == ((idx0 + 2000) % N) or idx == ((idx0 + 3000) % N):
    #         # print(I.v)
    #         ret += I.v
    # return ret

# class Item(object):
#     def __init__(self, v):
#         self.v = v
#     def __repr__(self):
#         return repr(self.v)

# def work_p1(inputs):
#     numbers = [int(l.strip()) for l in inputs]
#     numbers = [Item(n) for n in numbers]
#     N = len(numbers)
#     nmap = {numbers[i]:i for i in range(N)}
#     nmap_rev = {i:numbers[i] for i in range(N)}
    
#     for i in range(N):
#         I = numbers[i]
#         n = I.v
#         if n > 0:
#             for j in range(n):
#                 idx1 = nmap[I]
#                 idx2 = (idx1+1) % N
#                 J = nmap_rev[idx2]
#                 nmap[I] = idx2
#                 nmap[J] = idx1
#                 nmap_rev[idx1] = J
#                 nmap_rev[idx2] = I
#         elif n < 0:
#             for j in range(-n):
#                 idx1 = nmap[I]
#                 idx2 = (idx1-1) % N
#                 J = nmap_rev[idx2]
#                 nmap[I] = idx2
#                 nmap[J] = idx1
#                 nmap_rev[idx1] = J
#                 nmap_rev[idx2] = I

#     idx0 = None
#     for I, idx in nmap.items():
#         if I.v == 0:
#             idx0 = idx
#             break

#     ret = nmap_rev[(idx0+1000)%N].v
#     ret += nmap_rev[(idx0+2000)%N].v
#     ret += nmap_rev[(idx0+3000)%N].v

#     return ret

def work_p2(inputs):
    pass

def test_p1():
    assert(work_p1_p2(test_input, 1, 1) == 3)
test_p1()

def p1():
    print(work_p1_p2(fileinput.input(), 1, 1))
p1()

def test_p2():
    assert(work_p1_p2(test_input) == 1623178306)
test_p2()

def p2():
    print(work_p1_p2(fileinput.input()))
p2()
