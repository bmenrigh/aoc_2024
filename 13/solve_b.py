#!/usr/bin/python

import re
import math

button_re = re.compile(r'^Button\s([AB]):\sX\+(\d+),\sY\+(\d+)$')
prize_re = re.compile(r'Prize:\sX=(\d+),\sY=(\d+)$')


def solve_conf(config):
    a, b, p = config[0], config[1], config[2]

    xcf = math.gcd(a[0], b[0])
    ycf = math.gcd(a[1], b[1])

    lindep = False
    cf = math.gcd(xcf, ycf)
    agb = False
    if cf > 1:
        lindep == True
        if a[0] > b[0]:
            agb = True
        #print("non lin indep")
        #print(config)

    nn = (b[1] * p[0] - b[0] * p[1])
    nd = (a[0] * b[1] - b[0] * a[1])

    n = 0
    if nn % nd == 0:
        n = nn // nd

    mn = (a[1] * p[0] - a[0] * p[1])
    md = (b[0] * a[1] - a[0] * b[1])

    m = 0
    if mn % md == 0:
        m = mn // md

    if all([m != 0, n != 0]):
        if lindep:
            print(cf)
            print([n, m])

            if agb:
                if cf <= 3:
                    nq = n // cf
                    nr = n % cf

                    n_n = nr
                    n_m = m + cf * nq
                    print("agb converted to")
                    print([n_n, n_m])
                    return 3 * n_n + n_m
                else:
                    mq = m // cf
                    mr = m % cf

                    n_n = n + mq * cf
                    n_m = mr

                    print("agb with b -> a converted to")
                    print([n_n, n_m])
                    return 3 * n_n + n_m
            else:
                nq = n // cf
                nr = n % cf

                n_n = nr
                n_m = m + cf * nq
                print("bga converted to")
                print([n_n, n_m])
        else:
            return 3 * n + m

    return 0

step = 0
config = []
cost = 0
with open("input.txt") as lines:
    for line in lines:
        line = line.rstrip()

        if line == "":
            continue

        if step == 0:
            config = []

        #print(line)
        if step in [0, 1]:
            m = re.match(button_re, line)
            button = m.group(1)
            xd = int(m.group(2))
            yd = int(m.group(3))
            #print([button, xd, yd])
            step += 1
            config.append(tuple([xd, yd]))
            continue

        if step == 2:
            m = re.match(prize_re, line)
            px = int(m.group(1)) + 10000000000000
            py = int(m.group(2)) + 10000000000000
            config.append(tuple([px, py]))
            #print(config)
            cost += solve_conf(config)
            step = 0
            continue

print(cost)
