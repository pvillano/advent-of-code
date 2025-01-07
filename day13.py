import json
from functools import cmp_to_key
from itertools import (
    chain,
)

from utils import benchmark, debug_print, get_day, flatten

test = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

raw = get_day(13, test)
pair_str_list = raw.split("\n\n")


def in_order(left: list or int, right: list or int):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return "yes"
        if left > right:
            return "no"
        else:
            return "maybe"
    if isinstance(left, list) and isinstance(right, list):
        for li, ri in zip(left, right):
            tmp = in_order(li, ri)
            if tmp == "yes":
                return "yes"
            if tmp == "no":
                return "no"
        if len(left) < len(right):
            return "yes"
        if len(left) > len(right):
            return "no"
        else:
            return "maybe"
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    return in_order(left, right)


def part1():
    pairs = [[eval(line) for line in pair_str.split('\n')] for pair_str in pair_str_list]
    debug_print(pairs)
    tot = 0
    for idx, my_pair in enumerate(pairs):
        idx += 1
        tmp = in_order(*my_pair)
        if tmp == "yes":
            debug_print(idx, my_pair)
            tot += idx
    return tot


def part2():
    pairs = [[eval(line) for line in pair_str.split('\n')] for pair_str in pair_str_list]
    packets = flatten(pairs)
    packets = list(chain(packets, [[[2]]], [[[6]]]))

    for i in range(len(packets)):
        for j in range(len(packets) - 1):
            if in_order(packets[j], packets[j + 1]) == "no":
                tmp = packets[j], packets[j + 1]
                packets[j + 1], packets[j] = tmp

    debug_print()
    for x in packets:
        debug_print(x)
    i, j = packets.index([[2]]) + 1, packets.index([[6]]) + 1
    debug_print(i, j)
    return i * j


def part2v2():
    packets = [json.loads(line) for line in raw.split("\n") if line]
    packets.append([[2]])
    packets.append([[6]])

    def cmp(left, right):
        return {"yes": -1, "maybe": 0, "no": 1}[in_order(left, right)]

    packets = sorted(packets, key=cmp_to_key(cmp))

    debug_print()
    for x in packets:
        debug_print(x)

    i, j = packets.index([[2]]) + 1, packets.index([[6]]) + 1
    debug_print(i, j)
    return i * j


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
