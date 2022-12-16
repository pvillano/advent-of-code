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

from utils import benchmark, debug_print, get_day, pipe, debug_print_recursive, submit

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
    valves_dict = dict()
    for line in lines:
        name, rest = line.removeprefix("Valve ").split(" has flow rate=")
        rate, rest = rest.split("; ")
        rate = int(rate)
        rest = rest.removeprefix("tunnel leads to valve ").removeprefix("tunnels lead to valves ")
        childrent = rest.split(", ")
        # debug_print(f"{name=}, {rate=}, {childrent=}")
        assert name not in valves_dict
        valves_dict[name] = (rate, childrent)
    itoa = sorted(valves_dict.keys(), key=lambda x: (valves_dict[x][0], x), reverse=True)
    atoi = {ch: idx for idx, ch in enumerate(itoa)}
    weights = []
    edges = []
    for name in itoa:
        flow_rate, children = valves_dict[name]
        children = tuple(sorted(map(lambda x: atoi[x], children)))
        weights.append(flow_rate)
        edges.append(children)
    return tuple(weights), tuple(edges)


def part2():
    weights, edges = parse()

    """
    contribution is how much pressure can you release total, starting from here, with these valves unavailable
    
    equal to either using me and children with those plus me unavailable
    or not using me and with children with those plus me unavailable
    
    don't go backwards means you can't turn around unless you turn it on
    """

    @cache
    def dp(me=len(weights) - 1, ellie=len(weights) - 1, used: int = 0, time_left: int = 26):
        if time_left <= 1:
            return 0
        my_flow_rate, my_children = weights[me], edges[me]
        ellie_flow_rate, ellie_children = weights[ellie], edges[ellie]
        best = 0
        if my_flow_rate > 0 and not used & 1 << me:
            my_contrib = my_flow_rate * (time_left - 1)
            assert my_contrib >= 0
            my_used = used | 1 << me
            if ellie_flow_rate > 0 and not my_used & 1 << ellie:
                ellie_contrib = ellie_flow_rate * (time_left - 1)
                assert ellie_contrib >= 0
                tf2 = dp(me, ellie, my_used | 1 << ellie, time_left - 1)
                tf2 += my_contrib + ellie_contrib
                if tf2 > best:
                    best = tf2

            for ellie_child in ellie_children:
                tf2 = dp(me, ellie_child, my_used, time_left - 1)
                tf2 += my_contrib
                if tf2 > best:
                    best = tf2

        for my_child in my_children:
            if ellie_flow_rate > 0 and not used & 1 << ellie:
                ellie_contrib = ellie_flow_rate * (time_left - 1)
                assert ellie_contrib >= 0
                tf2 = dp(my_child, ellie, used | 1 << ellie, time_left - 1)
                tf2 += ellie_contrib
                if tf2 > best:
                    best = tf2

            for ellie_child in ellie_children:
                tf2 = dp(my_child, ellie_child, used, time_left - 1)
                if tf2 > best:
                    best = tf2
        return best

    for i in otqdm(range(27), percent_is_time=True, bars_is_time=True):
        dp(time_left=i)
    return dp()


def reparse(no_optimize=False) -> tuple[dict[str, list[str]], dict[tuple[str, str], int], dict[str, int]]:
    edges: dict[str, list[str]] = defaultdict(list)
    weights: dict[tuple[str, str], int] = dict()
    flows: dict[str, int] = dict()
    for line in lines:
        name, rest = line.removeprefix("Valve ").split(" has flow rate=")
        rate, rest = rest.split("; ")
        rate = int(rate)
        rest = rest.removeprefix("tunnel leads to valve ").removeprefix("tunnels lead to valves ")
        children = rest.split(", ")
        for child in children:
            edges[name].append(child)
            weights_key = min(name, child), max(child, name)
            weights[weights_key] = 1
            flows[name] = rate
    if no_optimize:
        return edges, weights, flows
    for parent in tuple(flows.keys()):
        if parent == "AA" or flows[parent] != 0:
            continue
        for child1, child2 in product(edges[parent], edges[parent]):
            # no loops, only do once
            if child1 <= child2:
                continue
            weights_key1 = min(parent, child1), max(parent, child1)
            weights_key2 = min(parent, child2), max(parent, child2)
            weights_key_new = min(child1, child2), max(child1, child2)
            weight = weights[weights_key1] + weights[weights_key2]
            if weights_key_new in weights:
                weight = min(weights[weights_key_new], weight)
            weights[weights_key_new] = weight
            del weights[weights_key1]
            del weights[weights_key2]
        for reverse_edge in edges[parent]:
            edges[reverse_edge].remove(parent)
        del edges[parent]
        del flows[parent]

    return edges, weights, flows


def part2v2():
    edges, weights, flow_rates = reparse(no_optimize=True)

    @cache
    def dp(me="AA", ellie="AA", used=frozenset(), my_time_left=26, ellie_time_left=26):
        best = 0
        if my_time_left >= ellie_time_left:
            if flow_rates[me] > 0 and me not in used and my_time_left > 1:
                my_contrib = flow_rates[me] * (my_time_left - 1)
                my_used = used.union([me])
                total_flow = dp(me, ellie, my_used, my_time_left - 1, ellie_time_left)
                total_flow += my_contrib
                if total_flow > best:
                    best = total_flow
            for my_child in edges[me]:
                weight_key = min(me, my_child), max(me, my_child)
                weight = weights[weight_key]
                assert weight > 0
                if my_time_left - weight > 1:
                    total_flow = dp(my_child, ellie, used, my_time_left - weight, ellie_time_left)
                    if total_flow > best:
                        best = total_flow
        else:
            if flow_rates[ellie] > 0 and ellie not in used and ellie_time_left > 1:
                ellie_contrib = flow_rates[ellie] * (ellie_time_left - 1)
                ellie_used = used.union([ellie])
                total_flow = dp(me, ellie, ellie_used, my_time_left, ellie_time_left - 1)
                total_flow += ellie_contrib
                if total_flow > best:
                    best = total_flow
            for ellie_child in edges[ellie]:
                weight_key = min(ellie, ellie_child), max(ellie, ellie_child)
                weight = weights[weight_key]
                assert weight > 0
                if ellie_time_left-weight > 1:
                    total_flow = dp(me, ellie_child, used, my_time_left, ellie_time_left-weight)
                    if total_flow >= best:
                        best = total_flow
        return best

    return dp()



if __name__ == "__main__":
    # benchmark(part1)
    # ans = benchmark(part2)
    ans = benchmark(part2v2)
