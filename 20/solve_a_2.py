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






def solve_maze(grid, start, end, max_cheat, min_imp, best):

    #beat_count = 0
    c_loc = {}

    def s_rec(cx, cy, s, mem, cheatx, cheaty, c_count, c_mem):

        nonlocal beat_count

        cbest = -1

        if not in_grid(cx, cy):
            return -1


        if grid[cx][cy] == "#":
            if c_count < max_cheat:
                c_count += 1

                if c_count == 1:
                    c_mem = {}
                    cheatx, cheaty = cx, cy
                    if not (cheatx, cheaty) in c_loc:
                        c_loc[(cheatx, cheaty)] = 0

            else:
                return -1

        if c_count == 0:
            if (cx, cy) in mem:
                if mem[(cx, cy)] <= s:
                    return -1
                else:
                    mem[(cx, cy)] = s
            else:
                mem[(cx, cy)] = s

        else:
            if (cx, cy) in mem:
                if mem[(cx, cy)] <= s:
                    return -1

            if (cx, cy) in c_mem:
                if c_mem[(cx, cy)] <= s:
                    return -1
                else:
                    c_mem[(cx, cy)] = s
            else:
                c_mem[(cx, cy)] = s


        #print(f"at ({cx}, {cy}) with score {s}")

        if (cx, cy) == end:
            if c_count > 0 and best > 0 and s <= best - min_imp:
                c_loc[(cheatx, cheaty)] += 1
            #print(f"found end in {s}")
            return s

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy

            ns = s_rec(nx, ny, s + 1, mem, cheatx, cheaty, c_count, c_mem)

            if ns > -1:
                if ns < cbest or cbest == -1:
                    cbest = ns

        return cbest


    best = s_rec(start[0], start[1], 0, {}, 0, 0, 0, None)

    c_grid = copy.deepcopy(grid)
    beat_count = 0
    for ct in c_loc:
        if c_loc[ct] > 0:
            beat_count += 1
            c_grid[ct[0]][ct[1]] = "@"

    #print_grid(c_grid)

    print(beat_count)

    return best


print_grid(grid)
print(start)
print(end)

best = solve_maze(grid, start, end, 0, 0, 0)
print(f"best to beat: {best}")
nb = solve_maze(grid, start, end, 1, 100, best)
#print(nb)


