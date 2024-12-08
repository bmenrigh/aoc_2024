#!/usr/bin/python

import copy

dstr = "^>v<"
xdl = [0, 1, 0, -1]
ydl = [-1, 0, 1, 0]

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append(list(line.rstrip()))

h = len(grid)
w = len(grid[0])

# find guard's starting location
(sx, sy) = (0, 0) # start x, y
sd = 0 # start direction
found = False

for y in range(0, h):

    if found:
        break

    for x in range(0, w):

        if grid[y][x] in dstr:
            (sx, sy) = (x, y)
            sd = dstr.index(grid[sy][sx])
            grid[sy][sx] = '.'
            found = True
            break
        elif grid[y][x] == ".":
            grid[y][x] = ""


def solve(cx, cy, d, ngrid):
    visited = copy.deepcopy(ngrid)

    dcount = 0
    while all([cx >= 0, cy >= 0, cx < w, cy < h]):

        if visited[cy][cx] != "X":
            dcount += 1
            visited[cy][cx] = "X"

        if dstr[d] in ngrid[cy][cx]:
            return -1, visited
        else:
            ngrid[cy][cx] += dstr[d]

        good = False
        (nx, ny) = (0, 0)
        while not good:
            (nx, ny) = (cx + xdl[d], cy + ydl[d])

            # If nx, ny in grid make sure it isn't an obstacle
            if all([nx >= 0, ny >= 0, nx < w, ny < h]):
                if ngrid[ny][nx] != "#":
                    good = True
                else:
                    d = (d + 1) % 4

            else:
                # Guard about to escape
                good = True

        (cx, cy) = (nx, ny)

    return dcount, visited


_, v_solve = solve(sx, sy, sd, copy.deepcopy(grid))

cycles = 0
for y in range(0, h):
    for x in range(0, w):
        if x != sx or y != sy:
            if v_solve[y][x] == "X":
                ngrid = copy.deepcopy(grid)
                ngrid[y][x] = "#"

                steps, _ = solve(sx, sy, sd, ngrid)

                if steps < 0:
                    cycles += 1

print(cycles)
