from collections import defaultdict
from functools import cache
from itertools import (
    combinations,
)

from utils import benchmark, debug_print, get_day
from utils.frozenbitset import bitset_factory_factory

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


def part1(frozenset_):
    valves = dict()
    for line in lines:
        name, rest = line.removeprefix("Valve ").split(" has flow rate=")
        rate, rest = rest.split("; ")
        rate = int(rate)
        rest = rest.removeprefix("tunnel leads to valve ").removeprefix("tunnels lead to valves ")
        descendants = rest.split(", ")
        debug_print(f"{name=}, {rate=}, {descendants=}")
        assert name not in valves
        valves[name] = (rate, descendants)
        if len(descendants) > 1:
            assert line == f"Valve {name} has flow rate={rate}; tunnels lead to valves {', '.join(descendants)}"
        else:
            assert line == f"Valve {name} has flow rate={rate}; tunnel leads to valve {', '.join(descendants)}"
    debug_print(valves)

    """
    contribution is how much pressure can you release total, starting from here, with these valves unavailable

    equal to either using me and children with those plus me unavailable
    or not using me and with children with those plus me unavailable
    """

    @cache
    def dp(me, used: frozenset_, time_left):
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
            used_me = used.union(frozenset_([me]))
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

    return dp("AA", frozenset_(), 30)


def reparse() -> dict[str, tuple[int, list[tuple[str, int], ...]]]:
    edges_str: dict[str, list[str]] = defaultdict(list)
    weights_str: dict[tuple[str, str], int] = dict()
    flows_str: dict[str, int] = dict()
    for line in lines:
        name, rest = line.removeprefix("Valve ").split(" has flow rate=")
        rate, rest = rest.split("; ")
        rate = int(rate)
        rest = rest.removeprefix("tunnel leads to valve ").removeprefix("tunnels lead to valves ")
        children = rest.split(", ")
        for child in children:
            edges_str[name].append(child)
            weights_key = min(name, child), max(child, name)
            weights_str[weights_key] = 1
            flows_str[name] = rate
    # optimize...
    for parent in tuple(flows_str.keys()):
        if parent == "AA" or flows_str[parent] != 0:
            continue
        for child1, child2 in combinations(edges_str[parent], 2):
            weights_key1 = min(parent, child1), max(parent, child1)
            weights_key2 = min(parent, child2), max(parent, child2)
            weights_key_new = min(child1, child2), max(child1, child2)
            weight = weights_str[weights_key1] + weights_str[weights_key2]
            if weights_key_new in weights_str:
                weight = min(weights_str[weights_key_new], weight)
                assert child1 in edges_str[child2]
                assert child2 in edges_str[child1]
            else:
                edges_str[child1].append(child2)
                edges_str[child2].append(child1)
            weights_str[weights_key_new] = weight
            del weights_str[weights_key1]
            del weights_str[weights_key2]
        for reverse_edge in edges_str[parent]:
            edges_str[reverse_edge].remove(parent)
        del edges_str[parent]
        del flows_str[parent]

    # flow_rate, (edge, weight), (edge, weight)
    ret = {}
    for nodes, edge_weight in weights_str.items():
        for first, second in [nodes, reversed(nodes)]:
            if first not in ret:
                ret[first] = (flows_str[first], [])
            ret[first][1].append((second, edge_weight))
    return ret


def part2(frozenset_):
    mega_dict = reparse()

    @cache
    def dp(me: str, ellie: str, used, my_time_left=26, ellie_time_left=26):
        assert my_time_left >= ellie_time_left
        best = 0
        flow_rate_me, edges_me = mega_dict[me]
        if flow_rate_me > 0 and me not in used and my_time_left > 1:
            my_time_left_new = my_time_left - 1
            my_contrib = flow_rate_me * my_time_left_new
            my_used = used | frozenset_([me])
            if my_time_left_new >= ellie_time_left:
                total_flow = dp(me, ellie, my_used, my_time_left_new, ellie_time_left)
            else:
                total_flow = dp(ellie, me, my_used, ellie_time_left, my_time_left_new)
            total_flow += my_contrib
            best = max(best, total_flow)

        for my_child, weight in edges_me:
            my_time_left_new = my_time_left - weight
            if my_time_left_new < 1:
                continue
            if my_time_left_new >= ellie_time_left:
                total_flow = dp(my_child, ellie, used, my_time_left_new, ellie_time_left)
            else:
                total_flow = dp(ellie, my_child, used, ellie_time_left, my_time_left_new)
            best = max(best, total_flow)
        return best

    return dp(me="AA", ellie="AA", used=frozenset_())


def part2a():
    return part2(frozenset)


def part2b():
    return part2(bitset_factory_factory())


if __name__ == "__main__":
    # benchmark(part1)
    print("part 2 frozenset")
    benchmark(part2a)
    print("part 2 bitset")
    benchmark(part2b)
