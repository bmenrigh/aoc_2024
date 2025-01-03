#!/usr/bin/python3

import sys
import re

fname = 'test_in.txt'

if len(sys.argv) > 1:
    fname = sys.argv[1]

con_re = re.compile(r'^(..)-(..)$')

network = {}
with open(fname, 'r') as lines:
    for line in lines:
        line = line.rstrip()

        m = re.match(con_re, line)

        if m is None:
            print(f"Failed to parse connection for line {line}")
            continue

        rc, lc = m.group(1), m.group(2)

        if not rc in network:
            network[rc] = {}

        if not lc in network:
            network[lc] = {}

        network[rc][lc] = True
        network[lc][rc] = True


def find_trips(network):

    trips = []

    for c1 in network:
        for c2 in filter(lambda x: x > c1, network[c1]):
            for c3 in filter(lambda x: x > c2, network[c2]):
                if c1 in network[c3]:
                    trips.append(tuple([c1, c2, c3]))


    return trips


def in_clique(network, clique, c):

    for q in clique:
        if not q in network[c]:
            return False

    return True


cliques = []
all_trips = find_trips(network)

for trip in all_trips:
    cliques.append(list(trip))

for c in network:
    for clique in cliques:
        if not c in clique:
            if in_clique(network, clique, c):
                clique.append(c)

biggest_clique = []
biggest_clique_size = -1
for clique in cliques:
    if len(clique) > biggest_clique_size or biggest_clique_size == -1:
        biggest_clique = clique
        biggest_clique_size = len(clique)

biggest_clique.sort()
print(f'Password: {",".join(biggest_clique)}')
