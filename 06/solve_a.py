#!/usr/bin/python

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
(cx, cy) = (0, 0) # current x, y
d = 0 # direction
found = False

for y in range(0, h):

    if found:
        break

    for x in range(0, w):

        if grid[y][x] in dstr:
            (cx, cy) = (x, y)
            d = dstr.index(grid[cy][cx])
            found = True
            break

dcount = 0
while all([cx >= 0, cy >= 0, cx < w, cy < h]):

    if grid[cy][cx] != "X":
        dcount += 1
        grid[cy][cx] = "X"

    good = False
    (nx, ny) = (0, 0)
    while not good:
        (nx, ny) = (cx + xdl[d], cy + ydl[d])

        # If nx, ny in grid make sure it isn't an obstacle
        if all([nx >= 0, ny >= 0, nx < w, ny < h]):
            if grid[ny][nx] != "#":
                good = True
            else:
                d = (d + 1) % 4

        else:
            # Guard about to escape
            good = True

    (cx, cy) = (nx, ny)

print(dcount)
