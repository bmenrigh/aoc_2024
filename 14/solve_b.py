#!/usr/bin/python

import copy
import re
import math
from sympy import factorint

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

blank = list(map(list, zip(*space)))

#print(len(space))
#print(len(space[0]))

def fill_space(space, steps):
    for rbot in rbot_list:
        cx, cy = rbot[0], rbot[1]

        cx = (cx + (steps * rbot[2])) % w
        cy = (cy + (steps * rbot[3])) % h

        space[cx][cy] += 1

def print_space(space, i):
    print(f"i = {i}")
    print("=" * w)
    for y in range(0, h):
        for x in range(0, w):
            if space[x][y] == 0:
                print(" ", end="")
            else:
                #print(space[x][y], end="")
                print("#", end="")
        print("")
    print("")


# def factorv(rbot):
#     return factorint(abs(rbot[2]) + abs(rbot[3]))



# vel = [0] * 1000
# for rbot in rbot_list:
#     vel[abs(rbot[2]) + abs(rbot[3])] += 1

# for i in range(0, 150):
#     print(i)
#     print("#" * vel[i])


# factors = {}
# for rbot in rbot_list:
#     f = factorv(rbot)

#     print(f)


# quad = [0, 0, 0, 0]
# for x in range(0, w):
#     for y in range(0, h):
#         if x == w // 2:
#             continue
#         if y == h // 2:
#             continue


#         lh = 0
#         if x > w // 2:
#             lh = 1

#         bh = 0
#         if y > h // 2:
#             bh = 1

#         q = bh * 2 + lh

#         quad[q] += space[x][y]

def fill_quads(space):
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

    return quad

#print(space)
#print(quad)
#print(quad[0] * quad[1] * quad[2] * quad[3])

# for i in range(0, 100000):
#     space = copy.deepcopy(blank)
#     fill_space(space, i)
#     quads = fill_quads(space)

#     half_sym = abs((quads[0] + quads[2]) - (quads[1] + quads[3]))
#     if half_sym < 100:
#         print_space(space, i)

i = 18
while True:
    space = copy.deepcopy(blank)
    fill_space(space, i)
    quads = fill_quads(space)

    print_space(space, i)

    i += 103
