#!/usr/bin/python

import copy

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append(list(line.rstrip()))

grid = list(map(list, zip(*grid)))

h = len(grid[0])
w = len(grid)


def ingrid(x, y):
    return all([x >= 0, y >= 0, x < w, y < h])


def findregion(cx, cy, cl, grid, ngrid):

    a, p = 0, 0

    if grid[cx][cy] == cl:
        a += 1
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
                    p += 1
                else:
                    if ngrid[nx][ny] != " ":
                        fa, fp = findregion(nx, ny, cl, grid, ngrid)
                        a, p = (a + fa), (p + fp)


    return a, p



score = 0
ngrid = copy.deepcopy(grid)
for x in range(0, w):
    for y in range(0, h):

        if grid[x][y] != ' ' and ngrid[x][y] != ' ':
            a, p = findregion(x, y, grid[x][y], grid, ngrid)
            score += a * p

print(score)



