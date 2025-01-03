#!/usr/bin/python3

import sys
import re
import copy

aseq_re = re.compile(r'[<>v^]+A+')

codes = []
with open(sys.argv[1], 'r') as lines:
    for line in lines:
        codes.append(line.rstrip())


def nums_code_to_coords(code):

    ncoords = {'7': (0, 0), '8': (1, 0), '9': (2, 0),
               '4': (0, 1), '5': (1, 1), '6': (2, 1),
               '1': (0, 2), '2': (1, 2), '3': (2, 2),
               ' ': (0, 3), '0': (1, 3), 'A': (2, 3)}

    return [ncoords[c] for c in code]


def arrows_code_to_coords(code):

    acoords = {' ': (0, 0), '^': (1, 0), 'A': (2, 0),
               '<': (0, 1), 'v': (1, 1), '>': (2, 1)}

    return [acoords[c] for c in code]


def smart_path_to_goal(cp, gp, blank):

    # "Smart" rules on direction order
    order = 0 # 0: hv; 1: vh

    hd, vd = gp[0] - cp[0], gp[1] - cp[1]

    hs, ls = '', ''

    if hd < 0: # going left
        hs = '<'
        # going left favors horizontal movement first
        order = 0
    else:
        hs = '>'
        # going right favors vertial movement first
        order = 1

    if vd < 0:
        vs = '^'
    else:
        vs = 'v'

    # Check if we'd hit the blank and swap order
    if order == 0:
        # Check horizontal
        if (gp[0], cp[1]) == blank:
            order = 1

    else:
        if (cp[0], gp[1]) == blank:
            order = 0

    hl = [hs] * abs(hd)
    vl = [vs] * abs(vd)

    arrows = []
    if order == 0:
        arrows = hl + vl + ['A']
    else:
        arrows = vl + hl + ['A']

    return arrows


def coords_to_arrows_smart(coords, cp, blank):

    arrows = []
    for gp in coords:
        arrows.extend(smart_path_to_goal(cp, gp, blank))
        cp = gp

    return "".join(arrows)


def solve_arrows_chunked(astr, mem):

    astr_l = []
    for asub in re.findall(aseq_re, astr):
        if asub in mem:
            astr_l.append(mem[asub])
            continue

        best_next = coords_to_arrows_smart(arrows_code_to_coords(asub), (2, 0), (0, 0))

        mem[asub] = best_next
        astr_l.append(mem[asub])

    return "".join(astr_l)


def count_arrows_rec(astr, l, mem):

    if (astr, l) in mem:
        return mem[(astr, l)]

    if l == 0:
        mem[(astr, l)] = len(astr)
        return len(astr)

    count = 0
    for asub in re.findall(aseq_re, astr):

        if (asub, l) in mem:
            count += mem[(asub, l)]
        else:
            nastr = solve_arrows_chunked(asub, mem)
            count += count_arrows_rec(nastr, l - 1, mem)

    mem[(astr, l)] = count

    return count



def count_code_shortest(code, mem, layers):
    coords = nums_code_to_coords(code)
    astr = coords_to_arrows_smart(coords, (2, 3), (0, 3))

    count = count_arrows_rec(astr, layers, mem)

    return count


cnum_re = re.compile(r'^0*(\d+)A?$')

mem = {}
score = 0
for code in codes:
    m = re.match(cnum_re, code)

    if not m is None:
        cnum = int(m.group(1))

        c = count_code_shortest(code, mem, 25)

        score += cnum * c

        print(f"Code {code} ({cnum}) len {c}")

print(score)
