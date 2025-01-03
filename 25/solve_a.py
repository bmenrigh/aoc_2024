#!/usr/bin/python3

import sys
import re

fname = 'test_in.txt'

if len(sys.argv) > 1:
    fname = sys.argv[1]

grids = open(fname, 'r').read().split("\n\n")

keys = []
locks = []

W, H = len((grids[0].split("\n"))[0]), len(grids[0].split("\n"))

print(f"Lock width {W} and height {H}")

for grid in grids:
    islock = None

    rows = grid.rstrip("\n").split("\n")


    for i in range(W):
        if rows[0][i] != rows[H - 1][i]:
            if rows[0][i] == '#':
                islock = True
            else:
                islock = False

            break


    if islock is None:
        print(f"Ambiguous grid: {grid}")
        continue

    cuts = [0] * W

    for r in rows:
        for i in range(W):
            if r[i] == '#':
                cuts[i] += 1

    if islock:
        locks.append(cuts)
    else:
        keys.append(cuts)

print(f"Got {len(keys)} keys and {len(locks)} locks")

fit = 0
for l in locks:
    for k in keys:
        for i in range(W):
            if l[i] + k[i] > H:
                break
        else:
            fit += 1

print(fit)

