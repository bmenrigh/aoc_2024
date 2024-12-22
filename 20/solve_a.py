#!/usr/bin/python

import copy
import sys

sys.setrecursionlimit(100000)

d_x = [0, 1, 0, -1]
d_y = [-1, 0, 1, 0]
start_d = 1

mustsave = 1
bestmem = {}

grid = []
with open("test_in.txt") as lines:
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
        if grid[x][y] in "^>v<.":
            grid[x][y] = " "

        if grid[x][y] == "S":
            start = (x, y)

        if grid[x][y] == "E":
            end = (x, y)


def print_grid(grid):
    for y in range(0, h):
        for x in range(0, w):
            print(grid[x][y], end="")
        print("")

print(start)
print(end)
#print_grid(grid)

def solve_maze(cgrid, cheat, savemem):

    cbs = -1

    def solve_rec(cgrid, cx, cy, ex, ey, cs, mem, cheat, cheated):

        nonlocal cbs

        #print(f"config cx: {cx}, cy: {cy}, cs: {cs}, memory size: {len(mem)}")

        cheating = False
        if [cx, cy] in cheat:
            cheating = True
            cheated += 1

        if cx == ex and cy == ey:
            if len(cheat) > 0 and cheated < 2:
                return -1
            else:
                return cs

        if cgrid[cx][cy] == "#":
            if not cheating:
                return -1

        ct = tuple([cx, cy])

        if ct in bestmem:
            if bestmem[ct] < cs:
                return -1

        if cheated >= 2:
            if ct in bestmem:
                if bestmem[ct] - mustsave <= cs:
                    return -1

        if ct in mem:
            if mem[ct] <= cs:
                return -1
            else:
                mem[ct] = cs
        else:
            mem[ct] = cs

        if cbs > 0 and cs > cbs:
            return -1

        for d in range(0, 4):
            nx, ny = cx + d_x[d], cy + d_y[d]

            s = solve_rec(cgrid, nx, ny, ex, ey, cs + 1, mem, cheat, cheated)

            if cbs < 0 and s > 0:
                #print(f"setting best score to {s}")
                cbs = s

            if cbs > 0 and s > 0 and s < cbs:
                #print(f"found new best score {s}")
                cbs = s


        return cbs

    mem = {}
    if savemem:
        mem = bestmem

    return solve_rec(cgrid, start[0], start[1], end[0], end[1], 0, mem, cheat, 0)



best = solve_maze(grid, [], True)

print(f"Best non-cheating score: {best} with bestmem size {len(bestmem)}")

count = 0

for y in range(1, w - 1):
    print(f"Searching row {y} of {h}", file=sys.stderr)
    for x in range(1, w - 1):

        if grid[x][y] != "#":
            continue

        for dx, dy in [(1, 0), (0, 1)]:

            if any([x + dx >= w - 1, y + dy >= h - 1]):
                continue

            nx, ny = x + dx, y + dy

            if grid[nx][ny] == "#":
                continue

            cheat = [[x, y], [nx, ny]]

            #print(f"Trying with cheat {cheat}")
            score = solve_maze(grid, cheat, False)
            #print(f"score {score} cheating {cheat}")

            if score <= (best - mustsave):
                #print(f"Found better path {score} while cheating with {cheat}", file=sys.stderr)
                count += 1

print(count)



