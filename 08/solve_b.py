#!/usr/bin/python

import copy
import math

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append(list(line.rstrip()))

h = len(grid)
w = len(grid[0])

def ingrid(w, h, a):
    return all([a[0] >= 0, a[1] >= 0, a[0] < w, a[1] < h])

def add_point(a, b):
    return (a[0] + b[0], a[1] + b[1])

def project_ant(a, b):
    d = (b[0] - a[0], b[1] - a[1])

    cf = math.gcd(d[0], d[1])

    d = (d[0] // cf, d[1] // cf)

    ants = [a]
    good = True

    cp = a
    while good:
        np = add_point(cp, d)

        if ingrid(w, h, np):
            ants.append(np)
            cp = np
        else:
            good = False

    return ants

alist = {}
for y in range(0, h):
    for x in range(0, w):

        ant = grid[y][x]

        if ant == "#":
            grid[y][x] = '.'

        if not ant in ".#":
            alist[ant] = alist.get(ant, [])
            alist[ant].append(tuple([x, y]))

antinodes = copy.deepcopy(grid)

dcount = 0
for ant in alist.keys():
    for i in range(0, len(alist[ant])):
        for j in range(0, len(alist[ant])):
            if i == j:
                continue

            ants = project_ant(alist[ant][i], alist[ant][j])

            for a in ants:
                if antinodes[a[1]][a[0]] != "#":
                    dcount += 1

                antinodes[a[1]][a[0]] = "#"

print(dcount)
