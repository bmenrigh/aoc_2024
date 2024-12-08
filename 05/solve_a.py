#!/usr/bin/python

sum = 0
rules = {}
inrules = True
with open("input.txt") as lines:
    for line in lines:
        if inrules:
            if line.rstrip() == "":
                inrules = False
                continue

            r = (line.rstrip()).split("|")
            rules[r[0]] = rules.get(r[0], []) + [r[1]]

        else:
            # In updates
            u = (line.rstrip()).split(",")
            got = {}

            if len(u) < 1:
                break

            if u[0] == "":
                break

            for p in u:
                got[p] = True

                if any([rp in got for rp in rules.get(p, [])]):
                    break

            else:
                sum += int(u[len(u) // 2])

print(sum)
