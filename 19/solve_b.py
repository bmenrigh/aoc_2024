#!/usr/bin/python

import re

towels = []
patterns = []


l = 0
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip("\n")

        l += 1

        if l == 1:
            towels = line.split(", ")
        else:
            if line == "":
                continue

            patterns.append(line)

towels_l = list(map(list, towels))
patterns_l = list(map(list, patterns))

towels_d = {}
max_t = 0
for t in towels:
    if len(t) > max_t:
        max_t = len(t)
    towels_d[t] = 0


#print(towels)
#print(patterns)
minsub = 30

#towel_re = re.compile("^(?:" + "|".join(towels) + ")+$")

def find_all_subs(towels_l, subs):
    global minsub

    for a in towels:
        for b in towels:
            for c in towels:
                combo = a + b + c
                if len(combo) < minsub:
                    minsub = len(combo)
                for n in range(3, minsub):
                    for o in range(0, len(combo) - n):
                        subs["".join(combo[o:o + n])] = 0

def pre_check_pat(pat, subs):
    for n in range(3, minsub):
        for o in range(0, len(pat) - n):
            if not "".join(pat[o:o + n]) in subs:
                return False

    return True


def match_pattern(pat, o, mem, memdac):

    pat_o_t = tuple([pat, o])

    if pat_o_t in mem:
        return mem[pat_o_t]

    if o == 0:
        if not match_dac(pat, memdac):
            mem[pat_o_t] = 0
            return 0

    if o >= len(pat):
        mem[pat_o_t] = 1
        return 1

    res = 0
    for t in towels:
        lt = len(t)
        if t == pat[o:o + lt]:
            res += match_pattern(pat, o + lt, mem, memdac)

    mem[pat_o_t] = res
    return res


def match_dac(pat, mem):
    #print(f"matching sub-pattern {pat}")

    if pat in mem:
        return mem[pat]

    if pat == "":
        mem[pat] = False
        return True

    if len(pat) <= max_t:
        if pat in towels_d:
            mem[pat] = True
            return True

    if len(pat) == 1:
        mem[pat] = False
        return False

    m = len(pat) // 2

    l = max(1, (m - max_t))
    u = min(len(pat), m + max_t + 1)

    for s in range(l, u):
        pr, pl = match_dac(pat[:s], mem), match_dac(pat[s:], mem)
        #print(f"sub match result {pr} and {pl}")
        if pr and pl:
            mem[pat] = True
            return True

    mem[pat] = False
    return False


# def match_pattern_re(pat):
#     m = re.match(towel_re, pat)

#     if m is None:
#         return False
#     else:
#         return True

#subs = {}
#find_all_subs(towels_l, subs)
#print(f"found {len(subs)} subs")

count = 0
mem = {}
memdac = {}
#patterns = ["rrbgbr"] + patterns
for p in patterns:
    #print(f"trying to match {p}")
    mcount = match_pattern(p, 0, mem, memdac)

    #print(f"pattern {p} matched")
    count += mcount

    #break


print(count)
