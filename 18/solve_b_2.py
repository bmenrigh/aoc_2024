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
    print("=" * w)
    for y in range(h):
        for x in range(w):
            if grid[x][y] == 0:
                print(".", end="")
            elif grid[x][y] <= l:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def ingrid(x, y):
    return all([x >= 0, y >= 0, x < w, y < h])


def solve_mitm(grid, l):
    mem = [{}, {}]
    foundq = [[[0, 0]], [[w - 1, h - 1]]]

    #grids = [copy.deepcopy(grid), copy.deepcopy(grid)]

    a, b = 0, 1

    at = tuple(foundq[a][0])
    mem[a][at] = 0
    bt = tuple(foundq[b][0])
    mem[b][bt] = 0

    while True:
        if len(foundq[a]) > 0:
            x, y = foundq[a].pop()

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if not ingrid(nx, ny):
                    continue

                v = grid[nx][ny]
                if v > 0 and v <= l:
                    continue

                nt = tuple([nx, ny])

                if nt in mem[b]:
                    return True

                if not nt in mem[a]:
                    mem[a][nt] = 0
                    foundq[a].append([nx, ny])
                    #grids[a][nx][ny] = "X"

            a, b = b, a

        else:
            return False




#print_grid(grid, 1024)
l, u = 1024, len(corrupt)
while l < u:
    m = l + ((u - l) // 2)

    cansolve = solve_mitm(grid, m)

    if cansolve:
        l = m + 1
    else:
        u = m

print(f"Failed to solve at limit {l} with corrupt byte {corrupt[l - 1]}")
