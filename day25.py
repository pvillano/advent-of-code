from itertools import product

from utils import benchmark, get_day, test
from utils.grids import transpose


def parse(raw: str):
    chunks = raw.split("\n\n")
    locks = []
    keys = []
    for chunk in chunks:
        lines = chunk.splitlines()
        if lines[0] == "#####":
            pins = transpose(lines)
            bits = [p.count(".") for p in pins]
            locks.append(bits)
        else:
            assert lines[0] == "....."
            pins = transpose(lines)
            bits = [p.count("#") for p in pins]
            keys.append(bits)
    return locks, keys


def part1(raw: str):
    locks, keys = parse(raw)
    s = 0
    for l, k in product(locks, keys):
        if all(li >= ki for li, ki in zip(l, k)):
            s += 1
    return s


test1 = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

expected1 = 3


def main():
    test(part1, test1, expected1)
    raw = get_day(25)
    benchmark(part1, raw)


if __name__ == "__main__":
    main()
