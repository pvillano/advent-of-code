from itertools import (
    product,
)

from utils import benchmark, debug_print, get_day, debug_print_grid

test = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

raw = get_day(14, test)
lines = raw.split("\n")


def part1():
    curve_list = []
    max_c, max_r = 0, 0
    for line in lines:
        curve = []
        for point in line.split(" -> "):
            col, row = list(map(int, point.split(",")))
            max_c = max(max_c, col + 1)
            max_r = max(max_r, row + 1)
            curve.append((col, row))
        curve_list.append(curve)

    debug_print(f"{max_c=} {max_r=}")

    grid = [['.'] * max_r for _ in range(max_c)]
    for curve in curve_list:
        for start, end in zip(curve, curve[1:]):
            for c, r in product(range(start[0], end[0] + 1), range(start[1], end[1] + 1)):
                grid[c][r] = '#'
            for c, r in product(range(end[0], start[0] + 1), range(end[1], start[1] + 1)):
                grid[c][r] = '#'
    debug_print_grid(grid)

    tot = 0
    while True:
        sand_c, sand_r = 500, 0
        while True:
            dropped = False
            for cand_c, cand_r in ((sand_c, sand_r + 1), (sand_c - 1, sand_r + 1), (sand_c + 1, sand_r + 1)):
                if not (cand_c in range(max_c) and cand_r in range(max_r)):
                    # off, going off sides always falls to infinity
                    return tot
                if grid[cand_c][cand_r] == '.':
                    # falls lower
                    sand_c, sand_r = cand_c, cand_r
                    dropped = True
                    break
            # wasn't able to fall off or settle
            if not dropped:
                grid[sand_c][sand_r] = 'o'
                tot += 1
                break


def part2():
    curve_list = []
    max_c, max_r = 0, 0
    for line in lines:
        curve = []
        for point in line.split(" -> "):
            col, row = list(map(int, point.split(",")))
            max_c = max(max_c, col + 1)
            max_r = max(max_r, row + 1)
            curve.append((col, row))
        curve_list.append(curve)
    max_r += 1
    max_c += max_r
    debug_print(f"{max_c=} {max_r=}")

    grid = [['.'] * max_r for _ in range(max_c)]
    for curve in curve_list:
        for start, end in zip(curve, curve[1:]):
            for c, r in product(range(start[0], end[0] + 1), range(start[1], end[1] + 1)):
                grid[c][r] = '#'
            for c, r in product(range(end[0], start[0] + 1), range(end[1], start[1] + 1)):
                grid[c][r] = '#'
    debug_print_grid(grid)

    tot = 0
    while True:
        sand_c, sand_r = 500, 0
        while True:
            dropped = False
            for cand_c, cand_r in ((sand_c, sand_r + 1), (sand_c - 1, sand_r + 1), (sand_c + 1, sand_r + 1)):
                if not (cand_c in range(max_c) and cand_r in range(max_r)):
                    # off, going off sides always falls to infinity
                    # FUUUUUCK
                    debug_print_grid(grid, override=True)
                    return -1
                if grid[cand_c][cand_r] == '.':
                    # falls lower
                    sand_c, sand_r = cand_c, cand_r
                    dropped = True
                    break
            # wasn't able to fall off or settle
            if not dropped:
                if (sand_c, sand_r) == (500, 0):
                    return tot + 1
                grid[sand_c][sand_r] = 'o'
                tot += 1
                break

            if cand_r == max_r - 1:
                grid[sand_c][sand_r] = 'o'
                tot += 1
                break


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
