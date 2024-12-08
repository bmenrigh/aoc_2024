#!/usr/bin/python

import re

mul_re = re.compile(r'mul\((\d+),(\d+)\)')
inst_re = re.compile(r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)')

inst_l = []
with open("input.txt") as lines:
    for line in lines:
        for m in re.finditer(inst_re, line):
            inst_l.append(m.group(0))

sum = 0
enabled = True
for inst in inst_l:
    if inst == "do()":
        enabled = True
    elif inst == "don't()":
        enabled = False
    else:
        if enabled:
            m = re.match(mul_re, inst)
            sum += int(m.group(1)) * int(m.group(2))


print(sum)
