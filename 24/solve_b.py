#!/usr/bin/python3

import sys
import re
import copy

fname = 'test_in.txt'

if len(sys.argv) > 1:
    fname = sys.argv[1]

wire_re = re.compile(r'^([a-z0-9]+):\s+([01])$')
gate_re = re.compile(r'^([a-z0-9]+)\s+(AND|OR|XOR)\s+([a-z0-9]+)\s+->\s+([a-z0-9]+)$')

wmax = 0
zmax = ""

def parse_wnum(w):

    if not w[0] in "xyz":
        return -1, ''

    if w[1] >= "0" and w[1] <= "9" and w[2] >= "0" and w[2] <= "9":
        return int(w[1:3]), w[0]
    else:
        return -1, ''


def read_cir_file(fname, wires, gates, traceback):

    global wmax
    global zmax

    with open(fname, 'r') as lines:
        for line in lines:
            line = line.rstrip()

            if line == '':
                continue

            mw = re.match(wire_re, line)

            if not mw is None:
                wires[mw.group(1)] = int(mw.group(2))

                wnum, wtype = parse_wnum(mw.group(1))
                if wnum > wmax:
                    wmax = wnum

                continue

            mg = re.match(gate_re, line)

            if not mg is None:
                gate = (mg.group(1), mg.group(2), mg.group(3), mg.group(4))
                gates.append(gate)
                traceback[gate[3]] = gate

                wnum, wtype = parse_wnum(mg.group(4))
                if wnum > wmax:
                    wmax = wnum
                    if wtype == 'z':
                        zmax = mg.group(4)


                continue

            print(f"Got unparsable line: {line}")



def run_cir(gates, wires):

    gates_todo = copy.copy(gates)
    wire_vals = copy.copy(wires)

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

    return zvals


def check_addr_cir(gates, wmax, oswaps, debug):

    gates_todo = copy.copy(gates)
    wire_vals = {}

    olast = -1

    for i in range(wmax):
        wire_vals[f"x{i :02d}"] = 1
        wire_vals[f"y{i :02d}"] = 1

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

                # Output swap
                if wr in oswaps:
                    #if debug:
                     #   print(f"swapping {wr} with {oswaps[wr]}")
                    wr = oswaps[wr]

                wire_vals[wr] = r

                wnum, wtype = parse_wnum(wr)

                if wnum >= 0 and wtype == 'z':

                    if wnum != olast + 1:
                        if debug:
                            print(f"Got output {wnum} too early (expected {olast + 1})")
                        return False
                    else:
                        olast += 1

                    if wnum == 0:
                        if r != 0:
                            if debug:
                                print(f"Output {wnum} not expected val 0")
                            return False
                    else:
                        if r != 1:
                            if debug:
                                print(f"Output {wnum} not expected val 1")
                            return False
            else:
                new_gates_todo.append(gate)

        gates_todo = new_gates_todo

    return True


def try_all_swaps(gates, wmax, debug):


    owires = [gate[3] for gate in gates]

    print(f"Found {len(owires)} output wires {owires}")

    def add_oswap_rec(depth, i, maxadd, oswaps):

        if depth >= maxadd:
            good = check_addr_cir(gates, wmax, oswaps, debug)

            if good:
                print(f"Found good cir with oswaps {oswaps}")

            return

        for o1 in range(i, len(owires)):

            if owires[o1] in oswaps:
                continue

            ow1 = owires[o1]

            for o2 in range(o1 + 1, len(owires)):

                if owires[o2] in oswaps:
                    continue

                ow2 = owires[o2]

                oswaps[ow1] = ow2
                oswaps[ow2] = ow1

                add_oswap_rec(depth + 1, o1 + 1, maxadd, oswaps)

                del oswaps[ow1]
                del oswaps[ow2]


    add_oswap_rec(0, 0, 4, {})


def gate_above(w, traceback, oswaps):

    if w in oswaps:
        w = oswaps[w]

    if w in traceback:
        return traceback[w]
    else:
        return None


def wires_above(w, traceback, oswaps, abv_cache):

    seen = {}

    def wires_above_rec(cw):

        if cw in seen:
            return [] # loop found
        else:
            seen[cw] = True

        if cw in abv_cache:
            return abv_cache[cw]

        g = gate_above(cw, traceback, oswaps)

        if not g is None:
            res = [g[0], g[2]] + wires_above_rec(g[0]) + wires_above_rec(g[2])
            abv_cache[cw] = res
            return res

        else:
            abv_cache[cw] = []
            return []

    return wires_above_rec(w)


def all_wires_above(traceback, oswaps):

    all_abv = {}

    abv_cache = {}
    for w in traceback:
        all_abv[w] = set(wires_above(w, traceback, oswaps, abv_cache))

    return all_abv


def get_x_wires(wlist):

    xwires = [w for w in wlist if w.find('x') == 0]
    xwires.sort()

    return xwires


def all_x_up_right(wlist):

    xwires = sorted(set(get_x_wires(wlist)))

    if len(xwires) == 0:
        return False, -1, -1

    firstxnum, _ = parse_wnum(xwires[0])
    lastxnum, _ = parse_wnum(xwires[-1])

    return lastxnum - firstxnum == len(xwires) - 1, firstxnum, lastxnum


def check_all_wires_above(traceback, oswaps, debug):

    all_abv = all_wires_above(traceback, oswaps)

    for w in all_abv:

        if len(all_abv[w]) == 0:
            if debug:
                printf(f"No wires above {w} due to loop.")
            return False

        good, nmin, nmax = all_x_up_right(all_abv[w])

        if w.find('z') == 0:
            znum, _ = parse_wnum(w)

            if znum == wmax:
                znum -= 1

            if not good or nmax != znum or nmin != 0:
                if debug:
                    print(f"Bad output {w} wire with x wires above {sorted(set(get_x_wires(all_abv[w])))}")
                return False

        else:
            if not good:
                if debug:
                    print(f"Bad internal {w} wire with x wires above {sorted(set(get_x_wires(all_abv[w])))}")
                return False

    return True


wires = {}
gates = []
traceback = {}

read_cir_file(fname, wires, gates, traceback)
print(f"Maximum io wire number {wmax} and max output {zmax}")


# check_all_wires_above(traceback, {}, False)

# oswaps = {}
# for o19swp in ("dgm", "cph"):

#     print(f"Candidate swaps with z19: {o19swp}")

#     oswaps["z19"] = o19swp
#     oswaps[o19swp] = "z19"

#     o10search = set(wires_above("z10", traceback, oswaps, {}) + ["z10"]) - set(wires_above("z07", traceback, oswaps, {}))
#     for o10a in o10search:
#         for o10swp in traceback:
#             if o10a == o10swp:
#                 continue

#             if o10a in oswaps or o10swp in oswaps:
#                 continue

#             oswaps[o10a] = o10swp
#             oswaps[o10swp] = o10a

#             good = check_all_wires_above(traceback, oswaps, False)

#             if good:
#                 print(f"Candidate swap {o10a} with {o10swp}")

#                 check_addr_cir(gates, wmax, oswaps, True)

#             del oswaps[o10a]
#             del oswaps[o10swp]

#     del oswaps["z19"]
#     del oswaps[o19swp]


# Look for bad wires based on gate types
bad_wires = []
for g in gates:

    (a, op, b, r) = g

    # output wires (except last) must come from XOR
    if r[0] == 'z':
        if r != zmax:
            if op != 'XOR':
                bad_wires.append(r)
                print(f"Bad z-output wire {r} from {op} gate (should be XOR)")
        else:
            if op != 'OR':
                bad_wires.append(r)
                print(f"Bad last output carry wire {r} from {op} gate (should be OR)")

        if op == 'XOR':
            if r != 'z00':
                if a[0] in 'xy' or b[0] in 'xy':
                    bad_wires.append(r)
                    print(f"Bad z-output wire {r} from XOR gate with x/y inputs")

    else:
        if op == 'XOR':
            if not (a[0] in 'xy' or b[0] in 'xy'):
                bad_wires.append(r)
                print(f"Bad XOR gate output wire {r}, gate must be connected to output")

    if op == 'OR':
        pga = traceback[a]
        pgb = traceback[b]

        if pga[1] != 'AND':
            bad_wires.append(a)
            print(f"Gate type {pga[1]} output wire {a} feeds into OR gate")

        if pgb[1] != 'AND':
            bad_wires.append(b)
            print(f"Gate type {pgb[1]} output wire {b} feeds into OR gate")

    if op == 'XOR':

        if not a[0] in 'xy':

            pga = traceback[a]


            if pga[1] == 'AND':
                if not pga[0] in ["x00", "y00"] and not pga[2] in ["x00", "y00"]:
                    bad_wires.append(a)
                    print(f"Gate type AND output wire {a} feeds into XOR gate")

        if not b[0] in 'xy':

            pgb = traceback[b]

            if pgb[1] == 'AND':
                if not pgb[0] in ["x00", "y00"] and not pgb[2] in ["x00", "y00"]:
                    bad_wires.append(b)
                    print(f"Gate type AND output wire {b} feeds into XOR gate")

print(",".join(sorted(list(set(bad_wires)))))

#for n in range(wmax + 1):
#    zw = f"z{n :02d}"
#    print(f'x wires above {zw}: {sorted(set(get_x_wires(all_abv[zw])))}')



#try_all_swaps(gates, wmax, False)
#check_addr_cir(gates, wmax, oswaps, True)




#zvals = run_cir(gates, wires)

def zvals_to_num(zvals):

    onum = 0
    pow2 = 1
    for zv in zvals:
        onum += pow2 * zv
        pow2 *= 2

    return onum

#print(onum)
