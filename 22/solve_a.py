#!/usr/bin/python3

import sys

fname = 'test_in.txt'

if len(sys.argv) > 1:
    fname = sys.argv[1]

secrets = []
with open(fname, 'r') as lines:
    for line in lines:
        secrets.append(int(line.rstrip()))


def next_num(x):

    x = ((x << 6) ^ x) & 0xFFFFFF
    x = ((x >> 5) ^ x)
    x = ((x << 11) ^ x) & 0xFFFFFF

    return x


def nth_num(x, n):

    cx = x

    for i in range(n):
        cx = ((cx << 6) ^ cx) & 0xFFFFFF
        cx = ((cx >> 5) ^ cx)
        cx = ((cx << 11) ^ cx) & 0xFFFFFF

        if cx == x:
            print(f"Found cycle of length {i + 1} for {x}")
            return nth_num(x, n % (i + 1))
    else:
        return cx


#print(next_num(123))

#print(nth_num(10, 2000))

score = 0
for s in secrets:
    score += nth_num(s, 2000)

print(score)
