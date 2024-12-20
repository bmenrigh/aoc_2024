#!/usr/bin/python

import copy
import re
import sys

sys.setrecursionlimit(100 * 100)

coord_re = re.compile(r"(\d+),(\d+)$")

h, w = 71, 71

grid = []
corrupt = []

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

        corrupt.append(tuple[x, y])
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

    if all([cx == w - 1, cy == h - 1]):
        return True

    if any([cx < 0, cy < 0, cx >= w, cy >= h]):
        return False

    if grid[cx][cy] > 0 and grid[cx][cy] <= l:
        return False

    ct = tuple([cx, cy])
    if not ct in mem:
        mem[ct] = s
    elif mem[ct] <= s:
        return False
    else:
        mem[ct] = s

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = cx + dx, cy + dy

        solved = solve(grid, s + 1, nx, ny, l, mem)
        if solved:
            return True




#print_grid(grid, 1024)
for l in range(1024, len(corrupt)):
    cansolve = solve(grid, 0, 0, 0, l, None)
    if not cansolve:
        print(f"Failed to solve at limit {l} with corrupt byte {corrupt[l - 1]}")
        break

