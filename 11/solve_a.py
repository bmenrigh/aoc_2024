#!/usr/bin/python

mem = {}

stones = []
with open("input.txt") as lines:
    for line in lines:
        stones = (line.rstrip()).split()
        break

def blink_list(stones, bleft):
    scount = 0
    for stone in stones:
        scount += blink(stone, bleft)

    return scount


def blink(stone, bleft):

    if bleft not in mem:
        mem[bleft] = {}

    if stone in mem[bleft]:
        return mem[bleft][stone]

    if bleft <= 0:
        mem[bleft][stone] = 1
        return mem[bleft][stone]

    if int(stone) == 0:
        mem[bleft][stone] = blink("1", bleft - 1)
        return mem[bleft][stone]

    if len(stone) % 2 == 0:
        mem[bleft][stone] = blink(str(int(stone[:len(stone)//2])), bleft - 1) + blink(str(int(stone[len(stone)//2:])), bleft - 1)
        return mem[bleft][stone]

    mem[bleft][stone] = blink(str(int(stone) * 2024), bleft - 1)
    return mem[bleft][stone]


scount = blink_list(stones, 25)
print(scount)
