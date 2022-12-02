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

test = """A Y
B X
C Z"""

lines = get_day(2, test).split("\n")


def part1():
    map_them = {val: idx for idx, val in enumerate("ABC")}
    map_you = {val: idx for idx, val in enumerate("XYZ")}
    score = 0
    for line in lines:
        them, you = line.split(" ")
        score += map_you[you] + 1
        if map_them[them] == map_you[you]:
            score += 3
        elif (map_them[them] + 1) % 3 == map_you[you]:
            score += 6
    return score


def part2():
    map_them = {val: idx for idx, val in enumerate("ABC")}
    map_you = {val: idx for idx, val in enumerate("XYZ")}
    map_move = {
        "X": -1,
        "Y": 0,
        "Z": 1,
    }
    win_points = {
        "X": 0,
        "Y": 3,
        "Z": 6,
    }
    you_to_pts = [1,2,3]
    score = 0
    for line in lines:
        them, you = line.split(" ")
        them_int = map_them[them]
        you_int = (map_move[you] + them_int) % 3
        score += win_points[you] + you_to_pts[you_int]
        debug_print("rps pts", you_to_pts[you_int])
        debug_print("win pts", win_points[you])

    return score

    pass


benchmark(part1)
benchmark(part2)
