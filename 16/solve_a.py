#!/usr/bin/python

import copy
import sys

sys.setrecursionlimit(100000)

d_x = [0, 1, 0, -1]
d_y = [-1, 0, 1, 0]
start_d = 1

mem = {}

grid = []
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip("\n")

        grid.append(list(line))

grid = list(map(list, zip(*grid)))

w = len(grid)
h = len(grid[0])

start = (0, 0)
end = (0, 0)
for x in range(0, w):
    for y in range(0, h):
        if grid[x][y] in "^>v<.":
            grid[x][y] = " "

        if grid[x][y] == "S":
            start = (x, y)

        if grid[x][y] == "E":
            end = (x, y)


def print_grid(grid):
    for y in range(0, h):
        for x in range(0, w):
            print(grid[x][y], end="")
        print("")

print(start)
print(end)
print_grid(grid)

gbs = -1

def solve_maze(cgrid, cx, cy, ex, ey, cs, d):

    global gbs

    if cx == ex and cy == ey:
        return cs

    if cgrid[cx][cy] == "#":
        return -1

    if cgrid[cx][cy] == "X":
        return -1

    if gbs > 0 and cs > gbs:
        return -1

    cl = tuple([cx, cy, d])
    if not cl in mem:
        mem[cl] = cs

    if cs > mem[cl]:
        return -1

    if cs < mem[cl]:
        mem[cl] = cs

    cgrid[cx][cy] = "X"

    for nd in [d, (d - 1) % 4, (d + 1) % 4]:
        nx, ny = cx + d_x[nd], cy + d_y[nd]

        si = 1
        if d != nd:
            si += 1000

        s = solve_maze(cgrid, nx, ny, ex, ey, cs + si, nd)

        if gbs < 0 and s > 0:
            print(f"setting best score to {s}")
            gbs = s

        if gbs > 0 and s > 0 and s < gbs:
            print(f"found new best score {s}")
            gbs = s

    cgrid[cx][cy] = " "
    return gbs

best = solve_maze(copy.deepcopy(grid), start[0], start[1], end[0], end[1], 0, 1)

print(best)

