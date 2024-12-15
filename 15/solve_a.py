#!/usr/bin/python

import re


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
            grid.append(list(line))
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

def push_box(d, x, y):

    if grid[x][y] == "#":
        return False

    if grid[x][y] == ".":
        return True

    if grid[x][y] == "@":
        print("error got @")
        print([x, y])

    good = False
    if grid[x][y] == "O":

        nx = x + d_x[d]
        ny = y + d_y[d]

        good = push_box(d, nx, ny)

        if good:
            grid[nx][ny] = grid[x][y]
            grid[x][y] = "."

    return good


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

    good = push_box(d, nx, ny)

    if good:
        grid[nx][ny] = "@"
        grid[cx][cy] = "."
        cx, cy = nx, ny


    step += 1
    #print(step)
    #print_grid(grid)


score = 0
for x in range(0, w):
    for y in range(0, h):
        if grid[x][y] == "O":
            score += 100 * y + x

print(score)
