#!/usr/bin/python

fstart = []
flen = []
estart = []
elen = []
blocks = []
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip()

        alt = list(map(int, list(line)))

        p = 0
        fnum = 0
        enum = 0
        o = 0
        for i in range(0, len(alt)):
            if i % 2 == 0:
                fstart.append(o)
                flen.append(alt[i])
                o += alt[i]
                blocks = blocks + [fnum] * alt[i]
                fnum += 1
            else:
                estart.append(o)
                elen.append(alt[i])
                o += alt[i]
                blocks = blocks + [-1] * alt[i]
                enum += 1

lf = len(flen) - 1
while lf > 0:
    # find the first free space that can fit this last file
    for ei in range(0, len(elen)):
        if flen[lf] <= elen[ei]:
            if fstart[lf] <= estart[ei]:
                break
            for i in range(0, flen[lf]):
                blocks[estart[ei] + i] = lf
                blocks[fstart[lf] + i] = -1
            fstart[lf] = estart[ei]
            estart[ei] += flen[lf]
            elen[ei] -= flen[lf]
            break
    lf -= 1

sum = 0
for i in range(0, len(blocks)):
    if blocks[i] != -1:
        sum += blocks[i] * i

print(sum)
