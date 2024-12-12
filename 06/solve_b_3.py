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


def solve(cx, cy, d, grid, visited, nvisit, checking, loopboxes, exx, exy):
    cycles = 0
    hit_ex_count = 0

    while ingrid(cx, cy):

        if dstr[d] in visited[cx][cy]:
            return -1

        if checking:
            if dstr[d] in nvisit[cx][cy]:
                return (-1 - hit_ex_count)
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

                hitex = False
                if all([checking, nx == exx, ny == exy]):
                    hit_ex_count += 1
                    hitex = True
                if grid[nx][ny] != "#" and not hitex:
                    good = True

                    if not checking:
                        if visited[nx][ny] == "":
                            if loopboxes[nx][ny] != '#':
                                nvisit = copy.deepcopy(visited)
                                esc = solve(cx, cy, (d + 1) % 4, grid, visited, nvisit, True, loopboxes, nx, ny)

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

cycles = solve(sx, sy, sd, grid, visited, nvisit, False, loopboxes, -1, -1)

print(cycles)
