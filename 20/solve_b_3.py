#!/usr/bin/python

import copy
import sys

sys.setrecursionlimit(100000)


mustsave = 1
bestmem = {}

grid = []
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip("\n")

        grid.append(list(line))

grid = list(map(list, zip(*grid)))

w = len(grid)
h = len(grid[0])

start = (0, 0)
end = (0, 0)
for x in range(0, w):
    for y in range(0, h):
        #if grid[x][y] in "^>v<.":
            #grid[x][y] = " "

        if grid[x][y] == "S":
            start = (x, y)

        if grid[x][y] == "E":
            end = (x, y)


def print_grid(grid):
    for y in range(0, h):
        for x in range(0, w):
            print(grid[x][y], end="")
        print("")

def in_grid(x, y):
    return all([x >= 0, y >= 0, x < w, y < h])


def dist_from(grid, sx, sy, dist):

    def dist_rec(cx, cy, s, mem):

        if not in_grid(cx, cy):
            return

        if grid[cx][cy] == "#":
            return

        if (cx, cy) in mem:
            if s >= mem[(cx, cy)]:
                return
            else:
                mem[(cx, cy)] = s
                dist[cx][cy] = s
        else:
            mem[(cx, cy)] = s
            dist[cx][cy] = s

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy

            dist_rec(nx, ny, s + 1, mem)

        return


    dist_rec(sx, sy, 0, {})


def count_with_cheats(dist_s, dist_e, max_cheat, must_save, best):

    count = 0

    for sx in range(0, w):
        for sy in range(0, h):

                sd = dist_s[sx][sy]

                if sd < 0:
                    continue

                if sd > best - must_save:
                    continue

                for ex in range(0, w):
                    for ey in range(0, h):

                        ed = dist_e[ex][ey]

                        if ed < 0:
                            continue

                        pl = abs(ex - sx) + abs(ey - sy)

                        if pl > max_cheat:
                            continue

                        tl = sd + pl + ed

                        if tl <= best - must_save:
                            count += 1

    return count


empty_dist = copy.deepcopy(grid)
for x in range(0, w):
    for y in range(0, h):
        empty_dist[x][y] = -1

dist_s = copy.deepcopy(empty_dist)
dist_e = copy.deepcopy(empty_dist)

#print_grid(grid)
print(start)
print(end)


dist_from(grid, start[0], start[1], dist_s)
dist_from(grid, end[0], end[1], dist_e)

best = dist_s[end[0]][end[1]]
print(f"Distance of end from start: {best}")


count = count_with_cheats(dist_s, dist_e, 20, 100, best)
print(f"Cheats count: {count}")
