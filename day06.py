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

test = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

line = get_day(6, test)


def part1():
    for idx, abcd in enumerate(zip(line[0:], line[1:], line[2:], line[3:])):
        if len(set(abcd)) == 4:
            return idx+4


def part2():
    for idx, abcd in enumerate(zip(*[line[i:] for i in range(14)])):
        if len(set(abcd)) == 14:
            return idx+14


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
