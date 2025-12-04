from copy import deepcopy

from utils import test, benchmark, get_input
from utils.itertools2 import degenerate
from utils.printing import debug_print


@degenerate
def parse(raw: str):
    return raw.splitlines()


def part1(raw: str):
    parsed = parse(raw)
    accessible = 0

    for row_number, row in enumerate(parsed):
        for col_number, cell in enumerate(row):
            if cell != '@':
                continue
            neighbours = -1
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    rr = row_number + dr
                    cc = col_number + dc
                    if (rr in range(len(parsed))
                            and cc in range(len(parsed[0]))
                            and parsed[rr][cc] == '@'):
                        neighbours += 1
            if neighbours < 4:
                accessible += 1
                debug_print(row_number, col_number)
        debug_print()
    return accessible


def part2(raw: str):
    parsed = [list(row) for row in parse(raw)]
    changed = True
    while changed:
        next_parsed = deepcopy(parsed)
        changed = False
        for row_number, row in enumerate(parsed):
            for col_number, cell in enumerate(row):
                if cell != '@':
                    continue
                neighbours = -1
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        rr = row_number + dr
                        cc = col_number + dc
                        if (rr in range(len(parsed))
                                and cc in range(len(parsed[0]))
                                and parsed[rr][cc] == '@'):
                            neighbours += 1
                if neighbours < 4:
                    next_parsed[row_number][col_number] = '.'
                    changed = True
        parsed = next_parsed
    return sum([sum([1 for _ in row if _ == '@']) for row in parse(raw)]) - sum(
        [sum([1 for _ in row if _ == '@']) for row in parsed])


test1 = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

expected1 = 13

test2 = test1
expected2 = 43


def main():
    raw = get_input(__file__)
    # test(part1, test1, expected1)
    # benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
