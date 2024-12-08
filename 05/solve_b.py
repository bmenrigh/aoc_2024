#!/usr/bin/python

import copy

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

            if len(u) < 1:
                break

            if u[0] == "":
                break

            done = False
            total_swaps = 0
            while not done:
                got = {}
                nu = copy.copy(u)
                swaps = 0
                for p in u:
                    got[p] = True

                    for rp in rules.get(p, []):
                        if rp in got:
                            nu[nu.index(p)], nu[nu.index(rp)] = nu[nu.index(rp)], nu[nu.index(p)]
                            swaps += 1

                else:
                    u = copy.copy(nu)
                    if swaps > 0:
                        total_swaps += swaps
                    else:
                        done = True

            if total_swaps > 0:
                sum += int(u[len(u) // 2])

print(sum)
