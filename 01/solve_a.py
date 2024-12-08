#!/usr/bin/python

list_l = []
list_r = []
with open("input.txt") as list_in:
    for line in list_in:
        (l, r) = line.split()
        list_l.append(int(l))
        list_r.append(int(r))

list_l.sort()
list_r.sort()

sum = 0
for pairs in zip(list_l, list_r):
    (l, r) = list(pairs)
    sum += abs(l - r)

print(sum)
