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

test = """"""

elves = get_day(1, test).split("\n\n")
bags = [[int(line) for line in elf.split("\n")] for elf in elves]


def part1():
    return max([sum(x) for x in bags])


def part2():
    elf_totals = [sum(x) for x in bags]
    best_elves = sorted(elf_totals)
    sum_top = sum(best_elves[-3:])
    return sum_top


benchmark(part1)
benchmark(part2)
