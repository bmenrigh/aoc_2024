#!/usr/bin/python3

import sys
import re

fname = 'test_in.txt'

if len(sys.argv) > 1:
    fname = sys.argv[1]

wire_re = re.compile(r'^([a-z0-9]+):\s+([01])$')
gate_re = re.compile(r'^([a-z0-9]+)\s+(AND|OR|XOR)\s+([a-z0-9]+)\s+->\s+([a-z0-9]+)$')

wire_vals = {}
gates_todo = []
with open(fname, 'r') as lines:
    for line in lines:
        line = line.rstrip()

        if line == '':
            continue

        mw = re.match(wire_re, line)

        if not mw is None:
            wire_vals[mw.group(1)] = int(mw.group(2))
            continue

        mg = re.match(gate_re, line)

        if not mg is None:
            gates_todo.append(tuple([mg.group(1), mg.group(2), mg.group(3), mg.group(4)]))
            continue

        print(f"Got unparsable line: {line}")


while len(gates_todo) > 0:
    new_gates_todo = []

    for gate in gates_todo:
        (w1, g, w2, wr) = gate

        if w1 in wire_vals and w2 in wire_vals:
            v1, v2 = wire_vals[w1], wire_vals[w2]
            r = 0
            if g == "AND":
                r = v1 & v2
            elif g == "OR":
                r = v1 | v2
            elif g == "XOR":
                r = v1 ^ v2
            else:
                print(f"Got invalid gate op {g}")

            wire_vals[wr] = r
        else:
            new_gates_todo.append(gate)

    gates_todo = new_gates_todo


zwires = [w for w in wire_vals if w.find('z') == 0]
zwires.sort()
zvals = [wire_vals[z] for z in zwires]

print(zvals)

onum = 0
pow2 = 1
for zv in zvals:
    onum += pow2 * zv
    pow2 *= 2

print(onum)
