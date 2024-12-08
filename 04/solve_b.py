#!/usr/bin/python

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append(list(line.rstrip()))

h = len(grid)
w = len(grid[0])

count = 0
for x in range(1, w - 1):
    for y in range(1, h - 1):
        if grid[y][x] != "A":
            continue

        cross = []
        for xd in (-1, 1):
            for yd in (-1, 1):
                cross.append(grid[y + yd][x + xd])

        if all([l in "MS" for l in cross]):
            if all([cross[0] != cross[3], cross[1] != cross[2]]):
                count += 1

print(count)
