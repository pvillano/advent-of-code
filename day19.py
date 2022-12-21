import concurrent.futures
import multiprocessing
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
from multiprocessing import Pool

import numpy as np

from otqdm import otqdm

from utils import benchmark, debug_print, debug_print_grid, debug_print_sparse_grid, get_day, pipe, extract_ints, \
    debug_print_recursive

test = """Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.""".replace("\n  ", " ")
fake_test = """Blueprint 1:
  Each ore robot costs 1 ore.
  Each clay robot costs 1 ore.
  Each obsidian robot costs 1 ore and 1 clay.
  Each geode robot costs 1 ore and 1 obsidian.""".replace("\n  ", " ")

raw = get_day(19, test)
lines = test.split("\n")


def build_within_budget(bluepint, build, budget):
    return not np.any(bluepint.dot(build) > budget)


def one_hot(k):
    ret = np.zeros(4, int)
    ret[k] = 1
    return ret


def build_list_iterator(blueprint: np.ndarray, resources: np.ndarray):
    build_list = np.zeros(4, int)
    defer = []
    for big_digit in reversed(range(4)):
        while build_within_budget(blueprint, np.add(one_hot(big_digit), build_list), resources):
            build_list[big_digit] += 1
    yield build_list
    # count down
    while any(build_list != np.zeros(4, int)):
        for borrow_digit in range(4):
            if build_list[borrow_digit] > 0:
                build_list[borrow_digit] -= 1
                break
        for j in reversed(range(borrow_digit)):
            while build_within_budget(blueprint, one_hot(j) + build_list, resources):
                build_list[j] += 1
        yield tuple(build_list)


def benchmark_blueprint(blueprint):
    # how many geodes can we extract with these resources?
    glob_best = [0]

    @cache
    def dp(robots=(1, 0, 0, 0), resources=np.zeros(4, int), remaining_time=24):
        # debug_print_recursive(f"{robots=} {resources=} {remaining_time=}")
        if glob_best[0] == 8:
            raise OverflowError()
        if remaining_time == 0:
            tmp = resources[-1]
            if tmp > glob_best[0]:
                glob_best[0] = tmp
                debug_print(f"{resources=} {robots=} {remaining_time=}")
            return tmp

        best = 0
        for build in build_list_iterator(blueprint, resources):
            remaining_resources = resources - blueprint.dot(build)
            assert not np.any(remaining_resources < 0)
            new_bots = np.add(robots, build)
            new_resources = np.add(remaining_resources, robots)
            candidate = dp(tuple(new_bots), tuple(new_resources), remaining_time - 1)
            if candidate > best:
                best = candidate
        return best

    return dp()


def parse():
    blueprints = dict()
    for line in lines:
        int_list = extract_ints(line)
        bp_number, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = map(int, int_list)
        # ore, clay, obs
        blueprints[bp_number] = np.array([
            [ore_ore, 0, 0, 0],
            [clay_ore, 0, 0, 0],
            [obsidian_ore, obsidian_clay, 0, 0],
            [geode_ore, 0, geode_obsidian, 0]]).T  # whoops
    return blueprints


def test():
    assert len(list(build_list_iterator(np.identity(4, int), np.array([5, 5, 5, 5])))) == 6 ** 4


def part1():
    blueprints = parse()
    try:
        return max([bp_number * benchmark_blueprint(blueprint) for bp_number, blueprint in blueprints.items()])
    except OverflowError:
        pass


def part2():
    pass


if __name__ == "__main__":
    test()
    benchmark(part1)
    # benchmark(part2)
