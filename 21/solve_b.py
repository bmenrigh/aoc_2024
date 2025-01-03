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

    return [arrows]


def coords_to_arrows_rec(coords, cp, blank):

    return coords_to_arrows_smart(coords, cp, blank)

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


def score_arrows(arrows, depth):

    all_arrows = [arrows]
    shortest = min(list(map(len, all_arrows)))

    for i in range(depth):
        new_all_arrows = []
        #print(f"Scoring {arrows} at depth {i} with up to {len(all_arrows)} checks to do")
        for narrows in all_arrows:
            if len(narrows) == shortest:
                coords = arrows_code_to_coords("".join(narrows))
                new_all_arrows += coords_to_arrows_rec(coords, (2, 0), (0, 0))

        all_arrows = copy.copy(new_all_arrows)
        shortest = min(list(map(len, all_arrows)))

    return shortest


def find_best_successor(asub):

    coords = arrows_code_to_coords("".join(asub))
    all_arrows = coords_to_arrows_rec(coords, (2, 0), (0, 0))

    best_arrows = []
    best_score = -1

    for arrows in all_arrows:
        score = score_arrows(arrows, 3)

        if score < best_score or best_score == -1:
            best_score = score
            best_arrows = arrows

    return "".join(best_arrows)


def solve_arrows_chunked(astr, mem):

    arrows = []
    for asub in re.findall(aseq_re, astr):
        if asub in mem:
            arrows.extend(mem[asub])
            continue
        #else:
            #print(f"No mem for {asub}")

        #coords = arrows_code_to_coords(asub)
        #all_arrows = coords_to_arrows_rec(coords, (2, 0), (0, 0))
        #shortest = min(list(map(len, all_arrows)))

        # for na in new_all_arrows:
        #     if len(na) == shortest:
        #         na_coords = arrows_code_to_coords("".join(na))
        #         na_all_arrows = coords_to_arrows_rec(na_coords, (2, 0), (0, 0))

        #         for na_na in na_all_arrows:
        #             na_na_len = len(na_na)
        #             if best_arrows_enc_len == -1 or na_na_len < best_arrows_enc_len:
        #                 best_arrows = na
        #                 best_arrows_enc_len = na_na_len

        best_next = find_best_successor(asub)

        mem[asub] = list(best_next)
        arrows.extend(mem[asub])

    return arrows


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
            arrows = solve_arrows_chunked(asub, mem)
            count += count_arrows_rec("".join(arrows), l - 1, mem)

    mem[(astr, l)] = count

    return count




def solve_code_shortest(code, mem, layers):
    coords = nums_code_to_coords(code)
    all_arrows = coords_to_arrows_rec(coords, (2, 3), (0, 3))

    shortest = min(list(map(len, all_arrows)))


    # for i in range(2):
    #     new_all_arrows = []
    #     for arrows in all_arrows:
    #         if len(arrows) == shortest:
    #             coords = arrows_code_to_coords("".join(arrows))
    #             new_all_arrows += coords_to_arrows_rec(coords, (2, 0), (0, 0))

    #     all_arrows = copy.copy(new_all_arrows)
    #     shortest = min(list(map(len, all_arrows)))

    for i in range(layers):
        new_all_arrows = []
        #print(f"layer {i} len to check {len(all_arrows)}")
        for arrows in all_arrows:
            if len(arrows) == shortest:
                astr = "".join(arrows)
                new_all_arrows.append(solve_arrows_chunked(astr, mem))

        all_arrows = copy.copy(new_all_arrows)
        shortest = min(list(map(len, new_all_arrows)))

    for arrows in all_arrows:
        if len(arrows) == shortest:
            return "".join(arrows)


def count_code_shortest(code, mem, layers):
    coords = nums_code_to_coords(code)
    all_arrows = coords_to_arrows_rec(coords, (2, 3), (0, 3))

    shortest = min(list(map(len, all_arrows)))

    best_count = -1
    for arrows in all_arrows:
        astr = "".join(arrows)
        count = count_arrows_rec(astr, layers, mem)

        if best_count == -1 or count < best_count:
            best_count = count

    return best_count


cnum_re = re.compile(r'^0*(\d+)A?$')

mem = {}


# score = 0
# for code in codes:
#     m = re.match(cnum_re, code)

#     if not m is None:
#         cnum = int(m.group(1))

#         astr = solve_code_shortest(code, mem, 2)

#         score += cnum * len(astr)

#         print(f"Code {code} ({cnum}) len {len(astr)} ({astr})")

# print(score)

# print("running test")
# test = ">>vvA"
# btest = find_best_successor(test)
# print(f"Best successor for {test} is {btest}")

score = 0
for code in codes:
    m = re.match(cnum_re, code)

    if not m is None:
        cnum = int(m.group(1))

        c = count_code_shortest(code, mem, 25)

        score += cnum * c

        print(f"Code {code} ({cnum}) len {c}")

print(score)


# for l in range(2, 25):
#     astr = solve_code_shortest("0", mem, l)

#     print(f"Code 0 len after {l} steps: {len(astr)} {astr}")

# test = solve_arrows_chunked("<<vvvA", {})
# print(test)
# test = solve_arrows_chunked("<<vvvAA", {})
# print(test)
# test = solve_arrows_chunked("<<vvvAAA", {})
# print(test)
# test = solve_arrows_chunked("<<vvvAAAA", {})
# print(test)

#all_arrows = coords_to_arrows_rec(nums_code_to_coords("029A"), (2, 3), (0, 3))

#for arrows in all_arrows:
#    print("".join(arrows))
