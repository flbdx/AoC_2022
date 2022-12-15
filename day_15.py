#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

test_input="""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_15"]

def parse_inputs(inputs):
    re_int = re.compile("([-]?[0-9]+)")
    sensors = set()
    beacons = set()
    closest_beacon = {}

    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers = list(map(int, re_int.findall(line)))
        sensors.add(tuple(numbers[0:2]))
        beacons.add(tuple(numbers[2:4]))
        closest_beacon[tuple(numbers[0:2])] = tuple(numbers[2:4])
    
    return (sensors, beacons, closest_beacon)

def manhattan(p1, p2):
    return sum(abs(p1[d] - p2[d]) for d in range(2))

def work_p1(inputs, target_row=2000000):
    sensors, beacons, closest_beacon = parse_inputs(inputs)
    clear_radius = {s: manhattan(s, closest_beacon[s]) for s in sensors}

    # find the intersection segments between the scanned row and the exclusion zones
    intersect = []
    for sensor in sensors:
        r = clear_radius[sensor]
        if abs(sensor[1] - target_row) > r:
            continue
        o = abs(sensor[1] - target_row)
        intersect.append((sensor[0] - (r-o), sensor[0] + (r-o)))
    intersect = sorted(intersect)

    # fuse the intersected segments
    segments = []
    for seg in intersect:
        if len(segments) == 0:
            segments.append(seg)
        else:
            sprev = segments[-1]
            if sprev[1] >= seg[0]:
                segments[-1] = (sprev[0], max(sprev[1], seg[1]))
            else:
                segments.append(seg)

    # number of excluded points minus beacons on the row
    res = sum(b-a+1 for a, b in segments)
    for b in beacons:
        if b[1] == target_row:
            res-=1

    return res

def work_p2(inputs, width=4000000):
    sensors, beacons, closest_beacon = parse_inputs(inputs)
    clear_radius = {s: manhattan(s, closest_beacon[s]) for s in sensors}

    # can do smarter. or just copy past the previous part
    for row in range(0, width + 1):

        intersect = []
        for sensor in sensors:
            r = clear_radius[sensor]
            if abs(sensor[1] - row) > r:
                continue
            o = abs(sensor[1] - row)
            # for part 2 we limit the segment to the scanned aread
            seg = (max(0, sensor[0] - (r-o)), min(sensor[0] + (r-o), width))
            intersect.append(seg)
        intersect = sorted(intersect)

        segments = []
        for seg in intersect:
            if len(segments) == 0:
                segments.append(seg)
            else:
                sprev = segments[-1]
                if sprev[1] >= seg[0]:
                    segments[-1] = (sprev[0], max(sprev[1], seg[1]))
                else:
                    segments.append(seg)
        if len(segments) != 1:
            return (segments[0][1] + 1) * 4000000 + row

def test_p1():
    assert(work_p1(test_input, 10) == 26)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(test_input, 20) == 56000011)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
