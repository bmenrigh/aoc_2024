#!/usr/bin/python

import re
import copy

reg_str = "ABC"
ireg = [0, 0, 0]
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
            ireg[ri] = int(v)

            continue

        m = re.match(prog_re, line)

        if not m is None:
            p = m.group(1)

            prog = list(map(int, p.split(",")))

            continue

        print("unparsable line")
        print(line)

print(prog)

def run(reg, prog, out, debug):

    icount = 0
    ip = 0
    done = False
    while not done:
        icount += 1

        if icount > 1000:
            done = True
            continue

        if ip >= len(prog):
            done = True
            continue

        op = prog[ip]
        larg = prog[ip + 1] # literal
        carg = larg # combo

        if larg > 3:
            carg = reg[larg - 4]

        if debug:
            print(f"\ndebug ip: {ip}, op: {op}, larg: {larg}, carg: {carg}, regs: {reg} regs8: {list(map(lambda x: x % 8, reg))}")

        # adv
        if op == 0:
            if debug:
                print(f"A = A // (2 ** {carg})")
            reg[0] = reg[0] // (2 ** carg)

        # bxl
        if op == 1:
            if debug:
                print(f"B = B xor {larg}")
            reg[1] = reg[1] ^ larg

        # bst
        if op == 2:
            if debug:
                print(f"B = {carg} % 8")
            reg[1] = carg % 8

        # jnz
        if op == 3:
            if reg[0] != 0:
                if debug:
                    print(f"jmp to {larg}")
                ip = larg
                continue

        # bxc
        if op == 4:
            if debug:
                print(f"B = B xor C")
            reg[1] ^= reg[2]

        # out
        if op == 5:
            if debug:
                print(f"outputting {carg % 8}")
            out.append(carg % 8)

        # bdv
        if op == 6:
            if debug:
                print(f"B = A // (2 ** {carg})")
            reg[1] = reg[0] // (2 ** carg)

        # cdv
        if op == 7:
            if debug:
                print(f"C = A // (2 ** {carg})")
            reg[2] = reg[0] // (2 ** carg)

        if debug:
            print(f"result regs: {reg} regs8: {list(map(lambda x: x % 8, reg))}")
        ip += 2

    return out


# for i in range(0, 10000000000):
#ireg[0] = (40171146966 * 16) + 3
#tout = run(copy.copy(ireg), prog, copy.copy(out), True)
#exit(0)
#      #print(tout)
#      if tout == [5]:
#          print(i)
#          break
#exit(0)

mem = {}
sol = {}

def rec_crack(a, l):

    if tuple([a, l]) in mem:
        return

    if l <= len(prog):
        print(f"searching for len {l} with {a}")

        for i in range(0, 8):
            ireg[0] = a * 8  + i
            tout = run(copy.copy(ireg), prog, copy.copy(out), False)

            if tout == prog[0 - l:]:
                na = ireg[0]

                if not tuple([na, l]) in sol:
                    print(f"got len {l} output {tout} with {na} (solution a * (2 ** 3) + {i})")
                    sol[tuple([na, l])] = 0

                rec_crack(na, l + 1)

        mem[tuple([a, l])] = 0

    else:
        print(f"solution: {a}")
        exit(0)


rec_crack(0, 1)

# a = 0
# l = 1
# while l <= len(prog):
    # print(f"searching for len {l} with {a}")
    # good = False
    # for i in range(0, 1024):
    #     ireg[0] = a * 8 + i
    #     tout = run(copy.copy(ireg), prog, copy.copy(out), False)

    #     if tout == prog[0 - l:]:
    #         a = ireg[0]
    #         print(f"got len {l} output {tout} with {a} (solution a * 8 + {i})")
    #         l += 1
    #         good = True
    #         break

    # print(f"searching for len {l} with {a}")
    # good = False
    # for e in range(0, 8):
    #     if good:
    #         break
    #     for i in range(0, 65536):
    #         ireg[0] = a * (2 ** e) + i
    #         tout = run(copy.copy(ireg), prog, copy.copy(out), False)

    #         if tout == prog[0 - l:]:
    #             a = ireg[0]
    #             print(f"got len {l} output {tout} with {a} (solution a * 8 + {i})")
    #             l += 1
    #             good = True
    #             break


    # if not good:
    #     print("falling back to more complex search")
    #     for j in range(0, 8):
    #         if good:
    #             break
    #         for i in range(0, 7):
    #             if good:
    #                 break
    #             for e in range(0, 8):
    #                 ireg[0] = (a + j) * (8 * 2 ** e) + i
    #                 #ireg[0] = (a) * 16 + i
    #                 tout = run(copy.copy(ireg), prog, copy.copy(out), False)

    #                 if tout == prog[0 - l:]:
    #                     a = ireg[0]
    #                     print(f"got len {l} output {tout} with {a} (i j e): {i} {j} {e}")
    #                     l += 1
    #                     good = True
    #                     break


#print(a)

ireg[0] = 156985331222018
tout = run(copy.copy(ireg), prog, copy.copy(out), True)
print(",".join(list(map(str, tout))))
