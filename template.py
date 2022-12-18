import operator
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

from utils import benchmark, debug_print, debug_print_grid, debug_print_sparse_grid, get_day, pipe

test = """"""

raw = get_day(DAYNUMBER, test)
lines = raw.split("\n")


def part1():
    pass


def part2():
    pass


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
