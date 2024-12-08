#!/usr/bin/python

import re

eq_re = re.compile(r'^(\d+):((?:\s+\d+)+)$')


def solve_rec(res, nlist, i, t):

    solutions = 0

    if t > res:
        return 0

    if i >= len(nlist):
        if t == res:
            return 1
        else:
            return 0

    solutions += solve_rec(res, nlist, i + 1, t + nlist[i])
    solutions += solve_rec(res, nlist, i + 1, t * nlist[i])
    solutions += solve_rec(res, nlist, i + 1, int(str(t) + str(nlist[i])))

    return solutions


sum = 0
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip()

        m = re.match(eq_re, line)

        if m is None:
            break

        res = int(m.group(1))
        n_l = m.group(2)

        nlist = list(map(int, n_l.split()))

        scount = solve_rec(res, nlist, 1, nlist[0])

        if scount > 0:
            sum += res


print(sum)
