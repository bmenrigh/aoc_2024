#!/usr/bin/python

xmas_str = "XMAS"

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append(list(line.rstrip()))

h = len(grid)
w = len(grid[0])

count = 0
for x in range(0, w):
    for y in range(0, h):
        for xd in (-1, 0, 1):
            for yd in (-1, 0, 1):
                for o in range(0, len(xmas_str)):
                    nx = x + o * xd
                    ny = y + o * yd

                    if any([nx < 0, ny < 0, nx >= w, ny >= h]):
                        break

                    if grid[ny][nx] != xmas_str[o]:
                        break

                else:
                    count += 1

print(count)
