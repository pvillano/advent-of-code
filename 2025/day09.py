from itertools import starmap

from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate, flatten
from utils.parsing import extract_ints
from utils.printing import debug_print_sparse_grid


@degenerate
def parse(raw: str):
    return map(extract_ints, raw.splitlines())


def part1(raw: str):
    r = parse(raw)
    a_max = 0
    for x0, y0 in r:
        for x1, y1 in r:
            a = abs(x1 - x0 + 1) * abs(y1 - y0 + 1)
            a_max = max(a_max, a)
    return a_max


def part2a(raw: str):
    r = parse(raw)
    lines = zip(r, r[1:] + [r[0]])
    lines = list(map(sorted, lines))
    a_max = 0
    debug_print_sparse_grid(r)
    for x0, y0 in r:
        for x1, y1 in r:
            a = abs(x1 - x0 + 1) * abs(y1 - y0 + 1)
            if a <= a_max:
                continue
            x_start, x_end = min(x0, x1), max(x0, x1)
            y_start, y_end = min(y0, y1), max(y0, y1)
            fail = False
            for [xx_start, yy_start], [xx_end, yy_end] in lines:
                if x_start <= xx_end and xx_start <= x_end and y_start <= yy_end and yy_start <= yy_end:
                    fail = True
                    break
            if fail:
                break
            a_max = a
    return a_max


def part2(raw: str):
    r = parse(raw)
    upper_bottom = (94525, 50422)
    lower_top = (94525, 48322)
    # upper
    best = 0
    for x, y in r:
        if x >= upper_bottom[0]: continue
        if y <= upper_bottom[1]: continue
        lower = upper_bottom[1]
        left = x
        right = upper_bottom[0]
        upper = y
        if any(left < a < right and lower < b < upper for a, b in r):
            continue
        best = max(best, (right - left + 1) * (upper - lower + 1))
    return best


test1 = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

expected1 = 50

test2 = test1
expected2 = 24


def experiment(raw):
    points = parse(raw)
    atoix = sorted([p[0] for p in points])
    atoiy = sorted([p[1] for p in points])
    itoax = {x: i for i, x in enumerate(atoix)}
    itoay = {x: i for i, x in enumerate(atoiy)}
    points2 = list(starmap(lambda x, y: (itoax[x], itoay[y]), points))
    debug_print_sparse_grid(points2, override=True)

    points3 = [(x // 100, y // 100) for x, y in points]

    debug_print_sparse_grid(points3, override=True)
    exit(0)


def main():
    raw = get_input(__file__)

    # experiment(raw)

    test(part1, test1, expected1)
    benchmark(part1, raw)

    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
