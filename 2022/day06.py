from itertools import (
    count,
    dropwhile,
)

from utils import benchmark, get_day

test = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

line = get_day(6, test)


def part1():
    for idx, abcd in enumerate(zip(line[0:], line[1:], line[2:], line[3:])):
        if len(set(abcd)) == 4:
            return idx + 4


def part2():
    for idx, abcd in enumerate(zip(*[line[i:] for i in range(14)])):
        if len(set(abcd)) == 14:
            return idx + 14


def extra():
    return next(
        dropwhile(
            lambda s: len(set(s)) <= 14, zip(count(14), *[line[i:] for i in range(14)])
        )
    )[0]


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
    benchmark(extra)
