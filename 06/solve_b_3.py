#!/usr/bin/python

import copy

dstr = "^>v<"
xdl = [0, 1, 0, -1]
ydl = [-1, 0, 1, 0]

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append(list(line.rstrip()))

# transpose grid so inices are x, y
grid = list(map(list, zip(*grid)))

h = len(grid)
w = len(grid[0])

# find guard's starting location
(sx, sy) = (0, 0) # start x, y
sd = 0 # start direction
found = False

for y in range(0, h):
    for x in range(0, w):

        if grid[x][y] in dstr:
            (sx, sy) = (x, y)
            sd = dstr.index(grid[sx][sy])
            grid[sx][sy] = ''
        elif not grid[x][y] in "#":
            grid[x][y] = ""

def ingrid(x, y):
    return all([x >= 0, y >= 0, x < w, y < h])


def solve(cx, cy, d, grid, visited, nvisit, checking, loopboxes):
    cycles = 0

    while ingrid(cx, cy):

        if checking:
            if dstr[d] in nvisit[cx][cy]:
                return -1
            else:
                nvisit[cx][cy] += dstr[d]
        else:
            if dstr[d] in visited[cx][cy]:
                return -1
            else:
                visited[cx][cy] += dstr[d]

        good = False
        (nx, ny) = (0, 0)
        while not good:
            (nx, ny) = (cx + xdl[d], cy + ydl[d])

            # If nx, ny in grid make sure it isn't an obstacle
            if ingrid(nx, ny):
                if grid[nx][ny] != "#":
                    good = True

                    if not checking:
                        if visited[nx][ny] == "":
                            if loopboxes[nx][ny] != '#':
                                nvisit = copy.deepcopy(visited)
                                ngrid = copy.deepcopy(grid)
                                ngrid[nx][ny] = '#'
                                esc = solve(cx, cy, (d + 1) % 4, ngrid, visited, nvisit, True, loopboxes)

                                if esc < 0:
                                    loopboxes[nx][ny] = '#'
                                    cycles += 1

                else:
                    d = (d + 1) % 4

            else:
                # Guard about to escape
                good = True

        (cx, cy) = (nx, ny)

    return cycles


blank = copy.deepcopy(grid)
for y in range(0, h):
    for x in range(0, w):
        blank[x][y] = ""

visited = copy.deepcopy(blank)
nvisit = copy.deepcopy(blank)
loopboxes = copy.deepcopy(grid)

cycles = solve(sx, sy, sd, grid, visited, nvisit, False, loopboxes)

print(cycles)
