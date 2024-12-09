#!/usr/bin/python

import copy

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append(list(line.rstrip()))

h = len(grid)
w = len(grid[0])

def ingrid(w, h, a):
    return all([a[0] >= 0, a[1] >= 0, a[0] < w, a[1] < h])

def project_ant(a, b):
    d = (b[0] - a[0], b[1] - a[1])
    return (b[0] + d[0], b[1] + d[1])

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

            a = project_ant(alist[ant][i], alist[ant][j])

            if ingrid(w, h, a):
                if antinodes[a[1]][a[0]] != "#":
                    dcount += 1

                antinodes[a[1]][a[0]] = "#"

print(dcount)
