#!/usr/bin/python

grid = []
with open("input.txt") as lines:
    for line in lines:
        grid.append(list(line.rstrip()))

h = len(grid)
w = len(grid[0])


def count_trails(x, y, lasth, nines):
    if any([x < 0, x >= w, y < 0, y >= h]):
        return

    curh = grid[y][x]

    if curh == '.':
        return

    curh = int(curh)

    if curh != lasth + 1:
        return

    if curh == 9:
        nines.append(tuple([x, y]))

    count_trails(x - 1, y, curh, nines)
    count_trails(x + 1, y, curh, nines)
    count_trails(x, y - 1, curh, nines)
    count_trails(x, y + 1, curh, nines)


tot_trails = 0
for y in range(0, h):
    for x in range(0, w):
        if grid[y][x] == '.':
            continue

        if int(grid[y][x]) == 0:
            nines = []
            count_trails(x, y, -1, nines)
            tot_trails += len(set(nines))


print(tot_trails)
