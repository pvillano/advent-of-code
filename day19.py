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

raw = get_day(19, fake_test)
lines = raw.split("\n")


def can_build(resources, cost, ):
    ret = []
    for r, c in zip(resources, cost):
        if c > r:
            return False
        else:
            ret.append(r - c)
    return ret


def plus(a, b):
    return tuple(map(sum, zip(a, b)))


def benchmark_blueprint(blueprint):
    # how many geodes can we extract with these resources?
    glob_best = (0, 0, 0, 0)

    @cache
    def dp(robots=(1, 0, 0, 0), resources=(0, 0, 0, 0), remaining_time=26):
        # debug_print_recursive(f"{robots=} {resources=} {remaining_time=}")
        if remaining_time == 0:
            return resources[-1]
        iter_resources = resources
        best = 0
        for gebot in count():
            if iter_resources:
                iter_resources1 = copy(iter_resources)
                for obbot in count():
                    if iter_resources1:
                        iter_resources2 = copy(iter_resources1)
                        for clbot in count():
                            if iter_resources2:
                                iter_resources3 = copy(iter_resources2)
                                for orbot in count():
                                    if iter_resources3:
                                        if obbot > 0:
                                            pass
                                        tmp = dp(plus(robots, (orbot, clbot, obbot, gebot)),
                                                 plus(iter_resources3, robots),
                                                 remaining_time - 1)
                                        if tmp > best:
                                            best = tmp
                                            # debug_print_recursive(f"{robots=} {resources=} {remaining_time=} {best=}")
                                    else:
                                        break
                                    iter_resources3 = can_build(iter_resources3, blueprint[0])
                            else:
                                break
                            iter_resources2 = can_build(iter_resources2, blueprint[1])
                    else:
                        break
                    iter_resources1 = can_build(iter_resources1, blueprint[2])
            else:
                break
            iter_resources = can_build(iter_resources, blueprint[3])
        return best

    return dp()


def parse():
    blueprints = dict()
    for line in lines:
        int_list = extract_ints(line)
        bp_number, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = map(int, int_list)
        # ore, clay, obs
        blueprints[bp_number] = [
            [ore_ore, 0, 0, 0],
            [clay_ore, 0, 0, 0],
            [obsidian_ore, obsidian_clay, 0, 0],
            [geode_ore, 0, geode_obsidian, 0]]
    return blueprints


def part1():
    blueprints = parse()
    best = 0
    for bp_number, blueprint in blueprints.items():
        tmp = benchmark_blueprint(blueprint)
        if tmp > best:
            best = tmp
    return best


def part2():
    pass


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
