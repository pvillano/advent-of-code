from functools import cache

from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate
from utils.parsing import extract_ints

import numpy as np

@degenerate
def parse(raw: str):
    *present_str_list, regions_str = raw.split("\n\n")
    presents = [p.splitlines()[1:] for p in present_str_list]
    regions = [extract_ints(line) for line in regions_str.splitlines()]
    regions = [((l, w), rest) for (l, w, *rest) in regions]
    return presents, regions

@degenerate
def make_masks(presents):
    for p in presents:
        pp = np.array([list(line) for line in p])
        ppp = pp == '#'
        yield ppp

def can_fit(length: int, width: int, presents: list[list[str]], counts: list[int]):
    masks = []
    for p in presents:
        pp = np.array([list(line) for line in p])
        ppp = pp == '#'
        masks.append(ppp)
    @cache
    def _can_fit(board, remaining):
        board = np.zeros(shape=(width, length), dtype=bool)
        # for rotation in rotations()
        # for x_offset in range():
        #     for y_offset in range():

    retval = _can_fit(tuple(counts))
    _can_fit.cache_clear()
    return retval

def part1(raw: str):
    presents, regions = parse(raw)
    for (length, width), counts in regions:
        can_fit(length, width, presents, counts)


def part2(raw: str):
    parse(raw)


def research(raw):
    presents, regions = parse(raw)
    masks = make_masks(presents)
    mask_sizes = [sum(sum(row) for row in mask) for mask in masks]
    def it():
        for (length, width), counts in regions:
            area = length * width
            used_area = sum(cnt * mask_sizes[i] for i, cnt in enumerate(counts))
            # print(f"{used_area: 4}\t{area: 4}\t{used_area / area}")
            yield used_area / area
    s = sorted(it())
    for i, ss in enumerate(s):
        print(i, ss)
    exit(0)


test1 = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

expected1 = None

test2 = test1
expected2 = None


def main():
    raw = get_input(__file__)

    research(raw)

    test(part1, test1, expected1)
    benchmark(part1, raw)

    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
