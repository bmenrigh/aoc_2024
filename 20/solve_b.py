#!/usr/bin/python

import copy
import sys

sys.setrecursionlimit(100000)


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






def solve_maze(grid, start, end, max_cheat, min_imp, best, c_loc, best_mem):

    def s_rec(cx, cy, px, py, s, mem, cheat_sx, cheat_sy, cheat_ex, cheat_ey, cheating, c_path, cheated, c_count, c_mem):

        cbest = -1

        if not in_grid(cx, cy):
            return -1

        if grid[cx][cy] == "#":
            if c_count < max_cheat and not cheated:
                #print(f"in # with c_count {c_count} at ({cx}, {cy})", flush=True)

                if c_count == 0:
                    #print(f"started cheating at ({cx}, {cy}) (actually ({px}, {py}))", flush=True)
                    cheating = True
                    c_path = {}
                    cheat_sx, cheat_sy = px, py
            else:
                return -1


        if cheated:
            if (cx, cy) in c_mem:
                if c_mem[(cx, cy)] <= s:
                    return -1
                else:
                    c_mem[(cx, cy)] = s
            else:
                c_mem[(cx, cy)] = s


        if cheating:
            c_count += 1

            #print(f"cheating at ({cx}, {cy})", flush=True)

            if (cx, cy) in c_path:
                if c_path[(cx, cy)] <= s:
                    return -1
                else:
                    c_path[(cx, cy)] = s
            else:
                c_path[(cx, cy)] = s

            if c_count >= max_cheat:
                if grid[cx][cy] == "#":
                    return -1
                cheating = False
                cheated = True
                cheat_ex, cheat_ey = cx, cy
                c_mem = {}
                if (cheat_sx, cheat_sy, cheat_ex, cheat_ey) not in c_loc:
                    c_loc[(cheat_sx, cheat_sy, cheat_ex, cheat_ey)] = 0

        if not cheating and not cheated:
            if (cx, cy) in mem:
                if mem[(cx, cy)] <= s:
                    return -1
                else:
                    mem[(cx, cy)] = s
            else:
                mem[(cx, cy)] = s

        if not cheating and not cheated and not best_mem is None:
            if (cx, cy) in best_mem:
                if s < best_mem[(cx, cy)]:
                    best_mem[(cx, cy)] = s
            else:
                best_mem[(cx, cy)] = s

        #print(f"at ({cx}, {cy}) with score {s}")

        if (cx, cy) == end:
            if cheated and c_count > 0 and best > 0 and s <= best - min_imp:
                c_loc[(cheat_sx, cheat_sy, cheat_ex, cheat_ey)] += 1
            #print(f"found end in {s}")
            return s

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy

            ns = s_rec(nx, ny, cx, cy, s + 1, mem, cheat_sx, cheat_sy, cheat_ex, cheat_ey, cheating, c_path, cheated, c_count, c_mem)

            if ns > -1:
                if ns < cbest or cbest == -1:
                    cbest = ns

        return cbest


    best = s_rec(start[0], start[1], -1, -1, 0, {}, 0, 0, 0, 0, False, None, False, 0, None)

    return best


print_grid(grid)
print(start)
print(end)

best_mem = {}
best = solve_maze(grid, start, end, 0, 0, 0, {}, None)
#print(best)
c_loc = {}
for i in range(0, 22):
    nb = solve_maze(grid, start, end, i, 100, best, c_loc, None)


c_grid = copy.deepcopy(grid)
beat_count = 0
for ct in c_loc:
    if c_loc[ct] > 0:
        beat_count += 1
        c_grid[ct[0]][ct[1]] = "1"
        c_grid[ct[2]][ct[3]] = "2"

print(beat_count)
print_grid(c_grid)
