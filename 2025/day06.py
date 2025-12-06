from functools import reduce

from utils import benchmark, test
from utils.advent import get_input
from utils.grids import rotate_counterclockwise, transpose, rotate_clockwise
from utils.itertools2 import degenerate


@degenerate
def parse(raw: str):
    for line in raw.splitlines()[:-1]:
        yield list(map(int, [x for x in line.split(' ') if x]))
    yield [x for x in raw.splitlines()[-1].split(' ') if x]


operators = {'+': lambda x, y: y + x, '-': lambda x, y: y - x, '*': lambda x, y: y * x, '/': lambda x, y: y / x,
             '^': lambda x, y: y ** x}


def part1(raw: str):
    unrotated = parse(raw)
    rotated = rotate_clockwise(unrotated)
    s = 0
    for problem in rotated:
        symbol, *operands = problem
        s += reduce(operators[symbol], operands)
    return s


def part2(raw: str):
    lines = raw.splitlines()
    cephup = rotate_counterclockwise(lines)
    s = 0
    stack = []
    for line in cephup:
        line = "".join(line).strip()
        if len(line) == 0:
            assert stack == []
        elif line[-1] in '+*':  # final in a comp
            stack.append(int("".join(line[:-1]).strip()))
            s += reduce(operators[line[-1]], stack)
            stack = []
        else:
            stack.append(int("".join(line).strip()))

    return s


test1 = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

expected1 = 4277556

test2 = test1
expected2 = 3263827


def main():
    raw = get_input(__file__)

    test(part1, test1, expected1)
    benchmark(part1, raw)

    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
