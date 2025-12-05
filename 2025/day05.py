from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate


@degenerate
def parse(raw: str):
    first, rest = raw.split('\n\n')

    def ranges():
        for r in first.splitlines():
            start, stop = r.split('-')
            yield range(int(start), int(stop) + 1)

    return list(ranges()), list(map(int, rest.splitlines()))


def part1(raw: str):
    ranges, ingredients = parse(raw)
    n = 0
    for ingredient in ingredients:
        if any(map(lambda r: ingredient in r, ranges)):
            n += 1
    return n


def part2(raw: str):
    ranges, _ = parse(raw)
    ranges.sort(key=lambda r: r.stop)
    # do the thing once it ends
    stack = [ranges[0]]
    for r in ranges[1:]:
        start, stop = r.start, r.stop
        while stack and start < stack[-1].stop and stack[-1].start < stop:
            final = stack.pop()
            start = min(final.start, start)
            stop = max(final.stop, stop)
        stack.append(range(start, stop))
    n = 0
    for r in stack:
        n += r.stop - r.start

    return n


test1 = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

expected1 = 3

test2 = test1
expected2 = 14

test22 = """0-0
1-1
2-2

1"""
expected22 = 3


def main():
    raw = get_input(__file__)
    test(part1, test1, expected1)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    test(part2, test22, expected22)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
