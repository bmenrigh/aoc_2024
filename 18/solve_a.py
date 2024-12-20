#!/usr/bin/python

import copy
import re
import sys

sys.setrecursionlimit(100 * 100)

coord_re = re.compile(r"(\d+),(\d+)$")

h, w = 71, 71

grid = []

for x in range(w):
    grid.append([0] * h)

time = 1
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip("\n")

        if line == "":
            continue
        m = re.match(coord_re, line)

        if m is None:
            continue

        x, y = int(m.group(1)), int(m.group(2))

        grid[x][y] = time
        time += 1


def print_grid(grid, l):
    for y in range(h):
        for x in range(w):
            if grid[x][y] == 0:
                print(".", end="")
            elif grid[x][y] <= l:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def solve(grid, s, cx, cy, l, mem):
    if s == 0:
        mem = {}

    if any([cx < 0, cy < 0, cx >= w, cy >= h]):
        return -1

    if grid[cx][cy] > 0 and grid[cx][cy] <= l:
        return -1

    ct = tuple([cx, cy])
    if not ct in mem:
        mem[ct] = s
    elif mem[ct] <= s:
        return -1
    else:
        mem[ct] = s

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = cx + dx, cy + dy

        solve(grid, s + 1, nx, ny, l, mem)

    if s == 0:
        et = tuple([w - 1, h - 1])
        if et in mem:
            return mem[et]
        else:
            return -1


print_grid(grid, 1024)
steps = solve(grid, 0, 0, 0, 1024, None)
print(steps)
