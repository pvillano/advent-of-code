from itertools import count

import scipy
from tqdm import tqdm

from utils import benchmark, test
from utils.advent import get_input
from utils.grids import transpose
from utils.itertools2 import degenerate
from utils.parsing import extract_ints


@degenerate
def parse(raw: str):
    for line in raw.splitlines():
        light_str, *buttons_str_list, joltage_str = line.split(' ')
        lights = int("".join(reversed(light_str[1:-1])).replace(".", '0').replace('#', '1'), base=2)
        buttons = []
        for button_str in buttons_str_list:
            buttons.append(sum(1 << int(i) for i in extract_ints(button_str)))
        joltages = extract_ints(joltage_str)
        yield lights, buttons, joltages


@degenerate
def parse2(raw: str):
    for line in raw.splitlines():
        _, *buttons_str_list, joltage_str = line.split(' ')
        buttons = []
        for button_str in buttons_str_list:
            buttons.append(extract_ints(button_str))
        joltages = extract_ints(joltage_str)
        yield buttons, joltages


def calc_cost(lights, buttons):
    seen = {0}
    costs = [[0]]
    for cur_cost in count(1):
        old_seen_length = len(seen)
        prev_costs = costs[-1]
        cur_costs = []
        for button in buttons:
            for parent in prev_costs:
                candidate = button ^ parent
                if candidate in seen:
                    continue
                if candidate == lights:
                    return cur_cost
                seen.add(candidate)
                cur_costs.append(candidate)
        costs.append(cur_costs)
        assert len(seen) > old_seen_length


def part1(raw: str):
    problems = parse(raw)

    def itercosts():
        for lights, buttons, _ in problems:
            x = calc_cost(lights, buttons)
            # print(x)
            yield x

    # sum(itercosts())
    # exit(0)

    return sum(itercosts())


def calc_cost2(joltages: tuple[int], button_indexes: list[tuple[int, ...]]):
    buttons = [[int(i in b) for i in range(len(joltages))] for b in button_indexes]
    seen = {tuple([0] * len(joltages))}
    prev_states = [tuple([0] * len(joltages))]
    for cur_cost in count(1):
        prev_len_seen = len(seen)
        next_states = []
        for button in buttons:  # does this loop order matter?
            for parent in prev_states:
                candidate = tuple(i + j for i, j in zip(button, parent))
                if candidate in seen:
                    continue
                if candidate == joltages:
                    return cur_cost
                seen.add(candidate)
                next_states.append(candidate)
        assert len(seen) > prev_len_seen
        prev_states = next_states


def calc_cost3(joltages: tuple[int], button_indexes: list[tuple[int, ...]]):
    buttons = [[int(i in b) for i in range(len(joltages))] for b in button_indexes]
    c = [1] * len(buttons)
    A_eq = transpose(buttons)
    b_eq = joltages

    result = scipy.optimize.linprog(c=c, A_eq=A_eq, b_eq=b_eq, method='highs', integrality=1)
    return result.fun


def part2(raw: str):
    s = 0
    for buttons, joltages in parse2(raw):
        s += calc_cost3(joltages, buttons)
    return s


test1 = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

expected1 = 7

test2 = test1
expected2 = 33


def main():
    raw = get_input(__file__)

    test(part1, test1, expected1)
    benchmark(part1, raw)

    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
