from collections import defaultdict, deque, Counter
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, reduce
from itertools import (
    accumulate,
    count,
    cycle,
    product,
    permutations,
    combinations,
    pairwise,
)
from math import sqrt, floor, ceil, gcd, sin, cos, atan2

from otqdm import otqdm

from utils import benchmark, debug_print, get_day, pipe

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
        first, second = line.split(',')
        l1, l2 = first.split("-")
        r1, r2 = second.split("-")
        l1, l2, r1, r2 = list(map(int, [l1, l2, r1, r2]))
        if l1 <= r1 <= r2 <= l2 or r1 <= l1 <= l2 <= r2:
            tot += 1
    return tot


def part2():
    tot = 0
    for line in lines:
        first, second = line.split(',')
        l1, l2 = first.split("-")
        r1, r2 = second.split("-")
        l1, l2, r1, r2 = list(map(int, [l1, l2, r1, r2]))
        if l1 <= r1 <= l2 or l1 <= r2 <= l2 or r1 <= l2 <= r2 or r1 <= l2 <= r2:
            tot += 1
    return tot


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
