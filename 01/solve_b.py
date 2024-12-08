#!/usr/bin/python

list_l = []
dict_r = {}
with open("input.txt") as list_in:
    for line in list_in:
        (l, r) = line.split()
        list_l.append(int(l))

        dict_r[int(r)] = dict_r.get(int(r), 0) + 1


sim = 0
for l in list_l:
    sim += l * dict_r.get(l, 0)

print(sim)
