#!/usr/bin/python

import itertools

safe = 0
with open("input.txt") as list_in:
    for line in list_in:
        l = map(int, line.split())

        deltas = [b - a for a, b in itertools.pairwise(l)]
        safeup = all([x > 0 and x < 4 for x in deltas])
        safedown = all([x < 0 and x > -4 for x in deltas])

        if any([safeup, safedown]):
            safe += 1

print(safe)
