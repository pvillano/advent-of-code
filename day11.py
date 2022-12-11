import operator
from dataclasses import dataclass
from functools import reduce
from math import lcm
from typing import Callable

from utils import benchmark, debug_print, get_day

test = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

raw = get_day(11, test)
monkies = raw.split("\n\n")


@dataclass
class Monkey:
    items: list[int]
    operation: Callable
    divisor: int
    if_true: int
    if_false: int
    inspect_count: int


def parsemonkey(monkey):
    lines = monkey.split("\n")
    assert len(lines) == 6
    items_str = lines[1].split(": ")[1]
    items = list(map(int, items_str.split(", ")))
    operation_str = lines[2].split("new = ")[1]
    op_fun = lambda x: eval(operation_str, {"old": x})
    test_divisor = int(lines[3].split()[-1])
    if_true = int(lines[4].split()[-1])
    if_false = int(lines[5].split()[-1])

    return Monkey(items, op_fun, test_divisor, if_true, if_false, 0)


def part1():
    my_monks: list[Monkey] = [parsemonkey(m) for m in monkies]
    for round_number in range(20):
        for idx, monkey in enumerate(my_monks):
            debug_print(f"Monkey {idx}:")
            for idx in range(len(monkey.items)):
                # inspect
                item = monkey.items[idx]
                debug_print(f"  Monkey inspects an item with a worry level of {item}.")
                item = monkey.operation(item)
                debug_print(f"    Worry level is to {item}.")
                item //= 3
                debug_print(f"    Monkey gets bored with item. Worry level is divided by 3 to {item}.")
                if (item % monkey.divisor) == 0:
                    debug_print(f"    Current worry level is divisible by {monkey.divisor}.")
                    my_monks[monkey.if_true].items.append(item)
                    debug_print(f"    Item with worry level {item} is thrown to monkey {monkey.if_true}.")
                else:
                    debug_print(f"    Current worry level is not divisible by {monkey.divisor}.")
                    my_monks[monkey.if_false].items.append(item)
                    debug_print(f"    Item with worry level {item} is thrown to monkey {monkey.if_true}.")
                monkey.inspect_count += 1
            monkey.items = list()
        debug_print(f"{round_number=}")
        for idx, monkey in enumerate(my_monks):
            debug_print(idx, monkey.items)
    for idx, monkey in enumerate(my_monks):
        debug_print(f"Monkey {idx} inspected items {monkey.inspect_count} times.")
    best_monks = sorted([m.inspect_count for m in my_monks])
    return best_monks[-1] * best_monks[-2]


def part2():
    my_monks: list[Monkey] = [parsemonkey(m) for m in monkies]
    mega_mod = reduce(lcm, [m.divisor for m in my_monks])
    for round_number in range(10000):
        for idx, monkey in enumerate(my_monks):
            for item in monkey.items:
                item = monkey.operation(item)
                item %= mega_mod
                if (item % monkey.divisor) == 0:
                    my_monks[monkey.if_true].items.append(item)
                else:
                    my_monks[monkey.if_false].items.append(item)
                monkey.inspect_count += 1
            monkey.items = list()
    for idx, monkey in enumerate(my_monks):
        debug_print(f"Monkey {idx} inspected items {monkey.inspect_count} times.")
    best_monks = sorted([m.inspect_count for m in my_monks])
    return best_monks[-1] * best_monks[-2]


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
