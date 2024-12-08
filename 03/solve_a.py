#!/usr/bin/python

import re

mul_re = re.compile(r'mul\((\d+),(\d+)\)')

sum = 0
with open("input.txt") as lines:
    for line in lines:
        for m in re.finditer(mul_re, line):
            sum += int(m.group(1)) * int(m.group(2))

print(sum)
