#!/usr/bin/python

import re

reg_str = "ABC"
reg = [0, 0, 0]
prog = []
out = []

reg_re = re.compile(r"^Register\s([A-C]):\s(\d+)$")
prog_re = re.compile(r"^Program:\s([\d,]+)$")

with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip("\n")

        if line == "":
            continue

        m = re.match(reg_re, line)

        if not m is None:
            r = m.group(1)
            v = m.group(2)

            ri = reg_str.index(r)
            reg[ri] = int(v)

            continue

        m = re.match(prog_re, line)

        if not m is None:
            p = m.group(1)

            prog = list(map(int, p.split(",")))

            continue

        print("unparsable line")
        print(line)

print(prog)

ip = 0
done = False
while not done:
    if ip >= len(prog):
        done = True
        continue

    op = prog[ip]
    larg = prog[ip + 1] # literal
    carg = larg # combo

    if larg > 3:
        carg = reg[larg - 4]

    print(f"debug ip: {ip}, op: {op}, larg: {larg}, carg: {carg}, regs: {reg}")

    # adv
    if op == 0:
        reg[0] = reg[0] // (2 ** carg)

    # bxl
    if op == 1:
        reg[1] = reg[1] ^ larg

    # bst
    if op == 2:
        reg[1] = carg % 8

    # jnz
    if op == 3:
        if reg[0] != 0:
            ip = larg
            continue

    # bxc
    if op == 4:
        reg[1] ^= reg[2]

    # out
    if op == 5:
        out.append(carg % 8)

    # bdv
    if op == 6:
        reg[1] = reg[0] // (2 ** carg)

    # cdv
    if op == 7:
        reg[2] = reg[0] // (2 ** carg)

    ip += 2

print(",".join(list(map(str, out))))
