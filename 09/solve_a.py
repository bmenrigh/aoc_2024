#!/usr/bin/python

blocks = []
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip()

        alt = list(map(int, list(line)))

        p = 0
        fnum = 0
        for i in range(0, len(alt)):
            if i % 2 == 0:
                blocks = blocks + [fnum] * alt[i]
                fnum += 1
            else:
                blocks = blocks + [-1] * alt[i]

s = 0
e = len(blocks) - 1

while s < e:
    if blocks[s] != -1:
        s += 1
        continue

    if blocks[e] == -1:
        e -= 1
        continue

    blocks[s], blocks[e] = blocks[e], blocks[s]


sum = 0
for i in range(0, len(blocks)):
    if blocks[i] != -1:
        sum += blocks[i] * i

print(sum)
