#!/usr/bin/python3

import sys

fname = 'test_in.txt'

if len(sys.argv) > 1:
    fname = sys.argv[1]

secrets = []
with open(fname, 'r') as lines:
    for line in lines:
        secrets.append(int(line.rstrip()))


def seq_num(x, n, loot):

    seen = {}

    cx = x

    pp = x % 10
    deltas = []
    for i in range(n):
        cx = ((cx << 6) ^ cx) & 0xFFFFFF
        cx = ((cx >> 5) ^ cx)
        cx = ((cx << 11) ^ cx) & 0xFFFFFF

        cp = cx % 10
        deltas.append(cp - pp)
        pp = cp

        deltas = deltas[-4:]

        if len(deltas) == 4:
            dt = tuple(deltas)

            if not dt in seen:
                seen[dt] = True

                loot[dt] = loot.get(dt, 0) + cp


loot = {}
for s in secrets:
    seq_num(s, 2000, loot)

best_score = 0
best_dt = (0, 0, 0, 0)
for dt, score in loot.items():
    if score > best_score:
        best_dt = dt
        best_score = score

print(f"Best score {best_score} with deltas {best_dt}")
