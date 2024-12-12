#!/usr/bin/python

import copy

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append([" "] + list(line.rstrip("\n")) + [" "])

grid.insert(0, [" "] * len(grid[0]))
grid.append([" "] * len(grid[0]))

grid = list(map(list, zip(*grid)))

h = len(grid[0])
w = len(grid)



def ingrid(x, y):
    return all([x >= 0, y >= 0, x < w, y < h])


def findregion(cx, cy, cl, grid, ngrid, sides):

    a, p = 0, 0

    if grid[cx][cy] == cl:
        a += 1
        sides[cx][cy] = "."
        ngrid[cx][cy] = " "

        for xd in [-1, 0, 1]:
            for yd in [-1, 0, 1]:
                if all([yd == 0, xd == 0]):
                    continue

                if not any([yd == 0, xd == 0]):
                    continue

                nx, ny = cx + xd, cy + yd

                if not ingrid(nx, ny):
                    p += 1
                elif grid[nx][ny] != cl:
                    if not sides is None:
                        sides[nx][ny] = "#"
                    p += 1
                else:
                    if ngrid[nx][ny] != " ":
                        fa, fp = findregion(nx, ny, cl, grid, ngrid, sides)
                        a, p = (a + fa), (p + fp)


    return a, p

def hasside_d(x, y, d, sides):
    if ingrid(x + d[0], y + d[1]):
        if sides[x][y] == ".":
            if sides[x + d[0]][y + d[1]] == "#":
                return True

    return False


def countsides(sides):
    s = 0

    for x in range(0, w):
        for xd in [-1, 1]:
            wallcont = False
            for y in range(0, h):
                inwall = hasside_d(x, y, (xd, 0), sides)
                if inwall and not wallcont:
                    s += 1
                wallcont = inwall

    for y in range(0, h):
        for yd in [-1, 1]:
            wallcont = False
            for x in range(0, w):
                inwall = hasside_d(x, y, (0, yd), sides)
                if inwall and not wallcont:
                    s += 1
                wallcont = inwall

    return s


def printgrid(grid):
        for y in range(0, h):
            for x in range(0, w):
                print(f"{grid[x][y]}", end="")
            print("")

#printgrid(grid)

blank = copy.deepcopy(grid)
for y in range(0, h):
    for x in range(0, w):
        blank[x][y] = " "

score = 0
ngrid = copy.deepcopy(grid)
for x in range(0, w):
    for y in range(0, h):

        if grid[x][y] != " " and ngrid[x][y] != " ":
            sides = copy.deepcopy(blank)
            a, p = findregion(x, y, grid[x][y], grid, ngrid, sides)

            s = countsides(sides)

            score += a * s
            #printgrid(sides)
            #print(str(a) + " * " + str(s))

print(score)



