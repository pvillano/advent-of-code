from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate


@degenerate
def parse(raw: str):
    for line in raw.splitlines():
        if line[0] == 'L':
            yield -int(line[1:])
        else:
            yield int(line[1:])
    return raw


def part1(raw: str):
    count = 0
    dial = 50
    for offset in parse(raw):
        dial += offset
        dial %= 100
        if dial == 0:
            count += 1
    return count


def part2(raw: str):
    count = 0
    dial = 50
    for offset in parse(raw):
        assert dial >= 0
        assert offset != 0
        next_dial = dial + offset
        if next_dial >= 100:
            count += next_dial // 100
        elif next_dial <= 0:
            count += (-next_dial) // 100
            if dial > 0:
                count += 1
        dial = next_dial % 100

    return count


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
