#!/usr/bin/python3

import sys
import re
import copy

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


def coords_to_arrows(coords, cp):

    arrows = []

    for gp in coords:

        while True:

            if cp == gp:
                arrows.append('A')
                break

            # direction priority >^v< (right, up, down, left)

            # > / right
            if cp[0] < gp[0]:
                cp = (cp[0] + 1, cp[1])
                arrows.append('>')
                continue

            # ^ / up
            if cp[1] > gp[1]:
                cp = (cp[0], cp[1] - 1)
                arrows.append('^')
                continue

            # v / up
            if cp[1] < gp[1]:
                cp = (cp[0], cp[1] + 1)
                arrows.append('v')
                continue

            # > / right
            if cp[0] > gp[0]:
                cp = (cp[0] - 1, cp[1])
                arrows.append('<')
                continue

    return arrows


def coords_to_arrows_rec(coords, cp, blank):

    all_arrows = []

    def solve_rec(cp, arrows, i, pd):

        if cp == blank:
            return

        if i >= len(coords):
            all_arrows.append(arrows)
            return

        if cp == coords[i]:
            solve_rec(cp, arrows + ['A'], i + 1, -1)
            return

        samedir = False
        if pd >= 0:

            if pd == 0 and cp[0] < coords[i][0]:
                samedir = True
                solve_rec((cp[0] + 1, cp[1]), arrows + ['>'], i, 0)

            if pd == 1 and cp[0] > coords[i][0]:
                samedir = True
                solve_rec((cp[0] - 1, cp[1]), arrows + ['<'], i, 1)

            if pd == 2 and cp[1] < coords[i][1]:
                samedir = True
                solve_rec((cp[0], cp[1] + 1), arrows + ['v'], i, 2)

            if pd == 3 and cp[1] > coords[i][1]:
                samedir = True
                solve_rec((cp[0], cp[1] - 1), arrows + ['^'], i, 3)

        if not samedir:

            if cp[0] < coords[i][0]:
                solve_rec((cp[0] + 1, cp[1]), arrows + ['>'], i, 0)

            if cp[0] > coords[i][0]:
                solve_rec((cp[0] - 1, cp[1]), arrows + ['<'], i, 1)

            if cp[1] < coords[i][1]:
                solve_rec((cp[0], cp[1] + 1), arrows + ['v'], i, 2)

            if cp[1] > coords[i][1]:
                solve_rec((cp[0], cp[1] - 1), arrows + ['^'], i, 3)

        return

    solve_rec(cp, [], 0, -1)

    return all_arrows


def solve_code(code):
    coords = nums_code_to_coords(code)
    arrows = coords_to_arrows(coords, (2, 3))

    astr = "".join(arrows)
    for i in range(2):
        coords = arrows_code_to_coords(astr)
        arrows = coords_to_arrows(coords, (2, 0))
        astr = "".join(arrows)

    return astr


def solve_code_shortest(code):
    coords = nums_code_to_coords(code)
    all_arrows = coords_to_arrows_rec(coords, (2, 3), (0, 3))

    shortest = min(list(map(len, all_arrows)))


    for i in range(2):
        new_all_arrows = []
        for arrows in all_arrows:
            if len(arrows) == shortest:
                coords = arrows_code_to_coords("".join(arrows))
                new_all_arrows += coords_to_arrows_rec(coords, (2, 0), (0, 0))

        all_arrows = copy.copy(new_all_arrows)
        shortest = min(list(map(len, all_arrows)))


    for arrows in all_arrows:
        if len(arrows) == shortest:
            return "".join(arrows)


cnum_re = re.compile(r'^0*(\d+)A?$')

score = 0
for code in codes:
    m = re.match(cnum_re, code)

    if not m is None:
        cnum = int(m.group(1))

        astr = solve_code_shortest(code)

        score += cnum * len(astr)

        print(f"Code {code} ({cnum}) len {len(astr)} ({astr})")

print(score)

#all_arrows = coords_to_arrows_rec(nums_code_to_coords("029A"), (2, 3), (0, 3))

#for arrows in all_arrows:
#    print("".join(arrows))
