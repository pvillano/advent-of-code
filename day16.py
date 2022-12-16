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

from utils import benchmark, debug_print, get_day, pipe, debug_print_recursive

test = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

raw = get_day(16, test)
lines = raw.split("\n")


# returns max flow


def part1():
    valves = dict()
    for line in lines:
        name, rest = line.removeprefix("Valve ").split(" has flow rate=")
        rate, rest = rest.split("; ")
        rate = int(rate)
        rest = rest.removeprefix("tunnel leads to valve ").removeprefix("tunnels lead to valves ")
        childrent = rest.split(", ")
        debug_print(f"{name=}, {rate=}, {childrent=}")
        assert name not in valves
        valves[name] = (rate, childrent)
        if len(childrent) > 1:
            assert line == f"Valve {name} has flow rate={rate}; tunnels lead to valves {', '.join(childrent)}"
        else:
            assert line == f"Valve {name} has flow rate={rate}; tunnel leads to valve {', '.join(childrent)}"
    debug_print(valves)
    # def recurse(me, ignored, used, time_left):
    #     # debug_print_recursive(f"recurse() {me=} {ignored=} {used=} {time_left=}")
    #     if time_left <= 0:
    #         yield 0
    #         return
    #
    #     flow_rate, children = valves[me]
    #
    #     if time_left <= 2 or len(used) == len(valves) - 1:
    #         yield flow_rate * (time_left - 1)
    #         return
    #
    #     if flow_rate > 0 and me not in used and me not in ignored:
    #         my_contrib = flow_rate * (time_left - 1)
    #         used_me = set(used)
    #         used_me.add(me)
    #         for child in children:
    #             # if child in used or child in ignored:
    #             #     continue
    #             for tf2 in recurse(child, ignored, used_me, time_left - 2):
    #                 yield tf2 + my_contrib
    #
    #     for child in children:
    #         ignored_me = set(ignored)
    #         ignored_me.add(me)
    #         # if child in used or child in ignored:
    #         #     continue
    #         for tf2 in recurse(child, ignored_me, used, time_left - 1):
    #             yield tf2 + 0
    #     yield flow_rate * (time_left - 1)
    #     return
    # best = 0
    # for x in recurse(me='AA', ignored=set(), used=set(), time_left=30):
    #     if x > best:
    #         best = x
    #         debug_print(x)

    """
    contribution is how much pressure can you release total, starting from here, with these valves unavailable
    
    equal to either using me and children with those plus me unavailable
    or not using me and with children with those plus me unavailable
    """

    @cache
    def dp(me, used: frozenset, time_left):
        if time_left <= 1:
            return 0, ()
        flow_rate, children = valves[me]
        if time_left <= 2 or len(used) == len(valves) - 1:
            if me not in used:
                return flow_rate * (time_left - 1), ((30 - time_left, me),)
            return 0, ()
        best = 0
        future = tuple()
        if flow_rate > 0 and me not in used:
            my_contrib = flow_rate * (time_left - 1)
            assert my_contrib > 0
            used_me = used.union(frozenset([me]))
            tf2, futureish = dp(me, used_me, time_left - 1)
            tf2 += my_contrib
            if tf2 > best:
                best = tf2
                future = ((30 - time_left, me),) + futureish
            best = max(best, tf2)
        for child in children:
            tf2, futureish = dp(child, used, time_left - 1)
            if tf2 > best:
                best = tf2
                future = futureish
        return best, future

    return dp("AA", frozenset(), 30)


def parse():
    valves = dict()
    for line in lines:
        name, rest = line.removeprefix("Valve ").split(" has flow rate=")
        rate, rest = rest.split("; ")
        rate = int(rate)
        rest = rest.removeprefix("tunnel leads to valve ").removeprefix("tunnels lead to valves ")
        childrent = rest.split(", ")
        # debug_print(f"{name=}, {rate=}, {childrent=}")
        assert name not in valves
        valves[name] = (rate, childrent)
    return valves


def part2():
    valves = parse()

    """
    contribution is how much pressure can you release total, starting from here, with these valves unavailable
    
    equal to either using me and children with those plus me unavailable
    or not using me and with children with those plus me unavailable
    
    don't go backwards means you can't turn around unless you turn it on
    """

    @cache
    def dp(me, ellie, used: frozenset, time_left):
        if time_left <= 1:
            return 0, ()
        my_flow_rate, my_children = valves[me]
        ellie_flow_rate, ellie_children = valves[ellie]
        best = 0
        future = tuple()
        if my_flow_rate > 0 and me not in used:
            my_contrib = my_flow_rate * (time_left - 1)
            assert my_contrib >= 0
            my_used = used.union(frozenset([me]))
            if ellie_flow_rate > 0 and ellie not in my_used:
                ellie_contrib = ellie_flow_rate * (time_left - 1)
                assert ellie_contrib >= 0
                tf2, futureish = dp(me, ellie, my_used.union(frozenset([ellie])), time_left - 1)
                tf2 += my_contrib + ellie_contrib
                if tf2 > best:
                    best = tf2
                    future = ((26 - time_left, "open", me, "open", ellie),) + futureish

            for ellie_child in ellie_children:
                tf2, futureish = dp(me, ellie_child, my_used, time_left - 1)
                tf2 += my_contrib
                if tf2 > best:
                    best = tf2
                    future = ((26 - time_left, "open", me, "to  ", ellie_child),) + futureish

        for my_child in my_children:
            if ellie_flow_rate > 0 and ellie not in used:
                ellie_contrib = ellie_flow_rate * (time_left - 1)
                assert ellie_contrib >= 0
                tf2, futureish = dp(my_child, ellie, used.union(frozenset([ellie])), time_left - 1)
                tf2 += ellie_contrib
                if tf2 > best:
                    best = tf2
                    future = ((26 - time_left, "to  ", my_child, "open", ellie),) + futureish

            for ellie_child in ellie_children:
                tf2, futureish = dp(my_child, ellie_child, used, time_left - 1)
                if tf2 > best:
                    best = tf2
                    future = ((26 - time_left, "to  ", my_child, "to  ", ellie_child),) + futureish
        return best, future

    return dp("AA", "AA", frozenset(), 26)


if __name__ == "__main__":
    # benchmark(part1)
    benchmark(part2)
