#!/usr/bin/python

import itertools

safe = 0
with open("input.txt") as list_in:
    for line in list_in:
        l = list(map(int, line.split()))

        deltas = [b - a for a, b in itertools.pairwise(l)]
        safeup_list = [x > 0 and x < 4 for x in deltas]
        safedown_list = [x < 0 and x > -4 for x in deltas]

        if any([all(safeup_list), all(safedown_list)]):
            safe += 1
        else:
            # try to fix by removing one
            if safeup_list.count(False) <= 2:
                bad_start = safeup_list.index(False)
                new_l_a = l[:bad_start] + l[bad_start + 1:]
                new_l_b = l[:bad_start + 1] + l[bad_start + 2:]

                new_deltas_a = [b - a for a, b in itertools.pairwise(new_l_a)]
                new_deltas_b = [b - a for a, b in itertools.pairwise(new_l_b)]

                if all([x > 0 and x < 4 for x in new_deltas_a]) or all([x > 0 and x < 4 for x in new_deltas_b]):
                    safe += 1

            elif safedown_list.count(False) <= 2:
                bad_start = safedown_list.index(False)
                new_l_a = l[:bad_start] + l[bad_start + 1:]
                new_l_b = l[:bad_start + 1] + l[bad_start + 2:]

                new_deltas_a = [b - a for a, b in itertools.pairwise(new_l_a)]
                new_deltas_b = [b - a for a, b in itertools.pairwise(new_l_b)]

                if all([x < 0 and x > -4 for x in new_deltas_a]) or all([x < 0 and x > -4 for x in new_deltas_b]):
                    safe += 1


print(safe)
