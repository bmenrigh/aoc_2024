#!/usr/bin/python

import copy
import re

w = 101
h = 103
steps = 100

rbot_re = re.compile(r'^p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)$')

rbot_list = []
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip("\n")

        m = re.match(rbot_re, line)

        if m is None:
            print("wtf!")
            print(line)
            break

        rbot = list(map(int, [m.group(1), m.group(2), m.group(3), m.group(4)]))

        rbot_list.append(rbot)


space = []

for y in range(0, h):
    space.append([0]*w)

space = list(map(list, zip(*space)))

#print(len(space))
#print(len(space[0]))


for rbot in rbot_list:
    cx, cy = rbot[0], rbot[1]

    cx = (cx + (steps * rbot[2])) % w
    cy = (cy + (steps * rbot[3])) % h

    space[cx][cy] += 1

quad = [0, 0, 0, 0]
for x in range(0, w):
    for y in range(0, h):
        if x == w // 2:
            continue
        if y == h // 2:
            continue


        lh = 0
        if x > w // 2:
            lh = 1

        bh = 0
        if y > h // 2:
            bh = 1

        q = bh * 2 + lh

        quad[q] += space[x][y]

#print(space)
#print(quad)
print(quad[0] * quad[1] * quad[2] * quad[3])
