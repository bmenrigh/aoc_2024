#!/usr/bin/python

import re

scale = {}
scale["#"] = "##"
scale["O"] = "[]"
scale["@"] = "@."
scale["."] = ".."


d_str = "^>v<"
d_x = [0, 1, 0, -1]
d_y = [-1, 0, 1, 0]

grid_re = re.compile(r"^#")
moves_re = re.compile(r"^[\^>v<]+$")


grid = []
moves = ""
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip("\n")

        if line == "":
            continue

        m = re.match(grid_re, line)

        if not m is None:
            ll = list(line)
            lll = list(map(lambda s: list(scale[s]), ll))
            grid.append([x for xs in lll for x in xs])

            continue

        m = re.match(moves_re, line)

        if not m is None:
            moves += line
            continue

        print("got unhandled line!!!")


grid = list(map(list, zip(*grid)))



h = len(grid[0])
w = len(grid)

def print_grid(grid):
    for y in range(0, h):
        for x in range(0, w):
            print(grid[x][y], end="")
        print("")

print_grid(grid)


def push_box(d, x, y, px, py, checking):
    #print(f"push_box at {x}, {y} grid symbol {grid[x][y]}")

    if grid[x][y] == "#":
        return False

    if grid[x][y] == ".":
        return True

    if grid[x][y] == "@":
        print("error got @")
        print([x, y])

    good = False
    if grid[x][y] in "[]":

        cxr, cyr, cyl, cyl = 0, 0, 0, 0
        nxl, nyl, nxr, nyr = 0, 0, 0, 0

        if grid[x][y] == "[":
            cxl, cyl = x, y
            cxr, cyr = x + 1, y
            nxl = cxl + d_x[d]
            nyl = cyl + d_y[d]
            nxr = cxr + d_x[d]
            nyr = cyr + d_y[d]
        else:
            cxl, cyl = x - 1, y
            cxr, cyr = x, y
            nxl = cxl + d_x[d]
            nyl = cyl + d_y[d]
            nxr = cxr + d_x[d]
            nyr = cyr + d_y[d]

        goodr = True
        goodl = True
        if all([any([nxr != px, nyr != py]), any([nxr != cxl, nyr != cyl])]):
            goodr = push_box(d, nxr, nyr, x, y, checking)

        if all([any([nxl != px, nyl != py]), any([nxl != cxr, nyl != cyr])]):
            goodl = push_box(d, nxl, nyl, x, y, checking)

        if not checking and all([goodr, goodl]):
            grid[nxl][nyl], grid[nxr][nyr] = grid[cxl][cyl], grid[cxr][cyr]
            if cxr != nxl and cyr != nyl:
                grid[cxr][cyr] = "."
            if cxl != nxr and cyl != nyr:
                grid[cxl][cyl] = "."

    return all([goodr, goodl])


cx, cy = -1, -1

for x in range(0, w):
    for y in range(0, h):
        if grid[x][y] == "@":
            cx, cy = x, y

print([cx, cy])

step = 0
for m in moves:
    d = d_str.index(m)

    nx, ny = cx + d_x[d], cy + d_y[d]

    good = push_box(d, nx, ny, nx, ny, True)

    if good:
        push_box(d, nx, ny, nx, ny, False)
        grid[nx][ny] = "@"
        grid[cx][cy] = "."
        cx, cy = nx, ny


    step += 1
    #print(step)
    #print_grid(grid)


score = 0
for x in range(0, w):
    for y in range(0, h):
        if grid[x][y] == "[":
            score += 100 * y + x

print(score)
