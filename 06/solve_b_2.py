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

    if found:
        break

    for x in range(0, w):

        if grid[x][y] in dstr:
            (sx, sy) = (x, y)
            sd = dstr.index(grid[sx][sy])
            grid[sx][sy] = '.'
            found = True
            break
        elif grid[x][y] == ".":
            grid[x][y] = ""



def solve(cx, cy, d, ngrid, visited, fr, lastturn):

    while all([cx >= 0, cy >= 0, cx < w, cy < h]):

        if dstr[d] in visited[cx][cy]:
            return -1
        else:
            visited[cx][cy] += dstr[d]

        good = False
        (nx, ny) = (0, 0)
        while not good:
            (nx, ny) = (cx + xdl[d] * fr, cy + ydl[d] * fr)

            # If nx, ny in grid make sure it isn't an obstacle
            if all([nx >= 0, ny >= 0, nx < w, ny < h]):
                if ngrid[nx][ny] != "#":
                    good = True
                else:
                    d = (d + fr) % 4
                    if fr == 1:
                        lastturn[0], lastturn[1], lastturn[2] = cx, cy, d

            else:
                # Guard about to escape
                good = True

        (cx, cy) = (nx, ny)

    return 0


def detect_loop(ox, oy, visit_for, visited):

    for d in range(0, len(dstr)):
        cx, cy = ox - xdl[d], oy - ydl[d]

        if all([cx >= 0, cy >= 0, cx < w, cy < h]):
            if dstr[d] in visit_for[cx][cy]:
                nd = (d + 1) % 4
                nx, ny = cx + xdl[nd], cy + ydl[nd]
                if all([nx >= 0, ny >= 0, nx < w, ny < h]):
                    if dstr[nd] in visited[nx][ny]:
                        return True

    return False


def need_backwards(ox, oy, visited, turns, lastturn):

    for d in range(0, len(dstr)):
        cx, cy = ox - xdl[d], oy - ydl[d]


        if all([cx >= 0, cy >= 0, cx < w, cy < h]):
            nd = (d + 1) % 4

            if all([cx == lastturn[0], cy == lastturn[1], nd == lastturn[2]]):
                continue

            nx, ny = cx + xdl[nd], cy + ydl[nd]
            if all([nx >= 0, ny >= 0, nx < w, ny < h]):
                if dstr[nd] in visited[nx][ny]:
                    if not all([cx == lastturn[0], cy == lastturn[1], d == lastturn[2]]):
                        turns.append(tuple([cx, cy, d]))
                    if not all([cx == lastturn[0], cy == lastturn[1], nd == lastturn[2]]):
                        turns.append(tuple([cx, cy, nd]))



blank = copy.deepcopy(grid)
for y in range(0, h):
    for x in range(0, w):
        blank[x][y] = ""

visited = copy.deepcopy(blank)

turns = [tuple([sx, sy, sd])]
lastturn = [0, 0, 0]
solve(sx, sy, sd, grid, visited, 1, lastturn)
print(lastturn)

v_forward = copy.deepcopy(visited)

for y in range(0, h):
    for x in range(0, w):
        if grid[x][y] == "#":
            need_backwards(x, y, visited, turns, lastturn)

for turn in turns:
    solve(turn[0], turn[1], turn[2], grid, visited, -1, None)





cycles = 0
for y in range(0, h):
    for x in range(0, w):
        if x != sx or y != sy:
            if v_forward[x][y] != "" and grid[x][y] != "#":

                if detect_loop(x, y, v_forward, visited):
                    cycles += 1

print(cycles)
