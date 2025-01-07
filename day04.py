import operator
from functools import reduce

from utils import benchmark, get_day

test = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

lines = get_day(4, test).split("\n")


def part1():
    tot = 0
    for line in lines:
        left, right = line.split(",")
        l1, l2 = left.split("-")
        r1, r2 = right.split("-")
        l1, l2, r1, r2 = map(int, [l1, l2, r1, r2])
        if l1 <= r1 <= r2 <= l2 or r1 <= l1 <= l2 <= r2:
            tot += 1
    return tot


def part2():
    tot = 0
    for line in lines:
        left, right = line.split(",")
        l1, l2 = left.split("-")
        r1, r2 = right.split("-")
        l1, l2, r1, r2 = map(int, [l1, l2, r1, r2])
        if l1 <= r1 <= l2 or l1 <= r2 <= l2 or r1 <= l2 <= r2 or r1 <= l2 <= r2:
            tot += 1
    return tot


def part2alt():
    tot = 0
    for line in lines:
        a, b, c, d = map(int, line.replace(',', '-').split('-'))
        if set(range(a, b + 1)) & set(range(c, d + 1)):
            tot += 1
    return tot


def part2alt2():
    s = '\n'.join(lines)
    return sum([bool(reduce(operator.and_, [set((lambda a, b: range(a, b + 1))(*map(int, elf.split("-")))) for elf in line.split(",")])) for line in s.split('\n')])


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
    benchmark(part2alt)
    benchmark(part2alt2)
