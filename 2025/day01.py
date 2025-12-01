from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate


@degenerate
def parse(raw: str):
    for line in raw.splitlines():
        yield line[0], int(line[1:])
    return raw


def part1(raw: str):
    cnt = 0
    p = 50
    for lr, x in parse(raw):
        if lr == 'L':
            p -= x
        else:
            p += x
        p %= 100
        if p == 0:
            cnt += 1
    return cnt


def part2(raw: str):
    cnt = 0
    p = 50
    for lr, x in parse(raw):
        if lr == 'L':
            dx = -1
        else:
            dx = 1
        for i in range(x):
            p += dx
            p %= 100
            if p == 0:
                cnt += 1
    return cnt


test1 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

expected1 = 3

test2 = test1
expected2 = 6


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
