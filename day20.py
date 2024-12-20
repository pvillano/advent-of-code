from collections import Counter, deque
from functools import cache
from itertools import product
from math import inf

import numpy as np
import z3
from tqdm import tqdm

from utils import benchmark, get_day, test
from utils.grids import grid_index, NEWS_RC, NESW_RC
from utils.parsing import extract_ints
from utils.printing import debug_print, debug_print_grid

__ = np, z3, tqdm, extract_ints, cache, Counter, deque


def parse(raw: str):
    grid = raw.splitlines()
    start = grid_index(grid, "S")
    end = grid_index(grid, "E")
    return start, end, grid


def part1(raw: str):
    start, end, grid = parse(raw)
    height, width = len(grid), len(grid[0])

    lch = [[inf] * len(row) for row in grid]
    lch[start[0]][start[1]] = 0
    q = deque([start])
    while q:
        r, c = q.pop()
        cost_here = lch[r][c]
        for dr, dc in NESW_RC:
            rr, cc = r + dr, c + dc
            if rr not in range(height) or cc not in range(width):
                continue
            if grid[rr][cc] == "#":
                continue
            if lch[rr][cc] > cost_here + 1:
                lch[rr][cc] = cost_here + 1
                q.appendleft((rr, cc))
    s = Counter()
    for r0, c0 in product(range(height), range(width)):
        if grid[r0][c0] != "#":
            continue
        cands = set()
        for dr, dc in NEWS_RC:
            rr, cc = r0 + dr, c0 + dc
            if rr not in range(height) or cc not in range(width):
                continue
            if grid[rr][cc] == "#":
                continue
            cands.add(lch[rr][cc])
        if not cands:
            continue
        start = min(cands)
        for c in cands:
            if c - start - 2 > 0:
                s[c - start - 2] += 1
    debug_print(sorted(s.items()))


def part2(raw: str):
    start, end, grid = parse(raw)
    height, width = len(grid), len(grid[0])

    lch = [[inf] * len(row) for row in grid]
    lch[start[0]][start[1]] = 0
    q = deque([start])
    while q:
        r, c = q.pop()
        cost_here = lch[r][c]
        for dr, dc in NESW_RC:
            rr, cc = r + dr, c + dc
            if rr not in range(height) or cc not in range(width):
                continue
            if grid[rr][cc] == "#":
                continue
            if lch[rr][cc] > cost_here + 1:
                lch[rr][cc] = cost_here + 1
                q.appendleft((rr, cc))
    s = Counter()
    debug_print_grid(lch)
    for r0, c0 in product(range(1, height - 1), range(1, width - 1)):
        start = lch[r0][c0]
        if start == inf:
            continue
        for dr, dc in product(range(-23, 23), range(-23, 23)):
            # for dr, dc in NEWS_RC:
            distance = abs(dr) + abs(dc)
            if distance > 20:
                continue
            rr, cc = r0 + dr, c0 + dc
            if not (rr in range(height) and cc in range(width)):
                continue
            if grid[rr][cc] == "#":
                continue
            c = lch[rr][cc]
            if c - start - distance > 0:
                s[c - start - distance] += 1
    debug_print([(k, v) for k, v in sorted(s.items())])
    debug_print([(k, v) for k, v in sorted(s.items()) if k >= 50])
    ret = sum(c for k, c in s.items() if k >= 100)
    assert ret != 997284
    return ret


test1 = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

expected1 = None

test2 = test1
expected2 = None


def main():
    test(part1, test1, expected1)
    raw = get_day(20)
    # benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
