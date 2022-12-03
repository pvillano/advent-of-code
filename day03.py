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

test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

lines = get_day(3, test).split("\n")


def part1():
    tot = 0
    for line in lines:
        first, second = line[:len(line)//2], line[len(line)//2:]
        assert len(first) == len(second)
        assert len(first) + len(second) == len(line)
        inboth = set(first) & (set(second))
        debug_print(inboth)
        for c in inboth:
            if ord('a') <= ord(c) <= ord('z'):
                tot += ord(c) - ord('a') + 1
            else:
                tot += ord(c) - ord('A') + 27
    return tot


def part2():
    groups = zip(lines[0::3], lines[1::3], lines[2::3], )
    groups = list(groups)
    debug_print(list(groups))
    tot = 0
    for g1, g2, g3 in groups:
        inall = (set(g1) & set(g2)) & set(g3)
        debug_print(inall)
        for c in inall:
            if ord('a') <= ord(c) <= ord('z'):
                tot += ord(c) - ord('a') + 1
            else:
                tot += ord(c) - ord('A') + 27
    return tot



if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
