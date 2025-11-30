from collections import Counter, deque
from itertools import product
from math import inf

from utils import benchmark, get_input, test
from utils.grids import grid_index, NEWS_RC, NESW_RC
from utils.parsing import extract_ints
from utils.printing import debug_print, debug_print_grid


def parse(raw: str):
    grid = raw.splitlines()
    start = grid_index(grid, "S")
    end = grid_index(grid, "E")

    lch = [[inf] * len(row) for row in grid]
    lch[start[0]][start[1]] = 0
    height, width = len(grid), len(grid[0])
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
    return start, end, grid, lch, width, height


def part1(raw: str):
    start, end, grid, lch, width, height = parse(raw)
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
    return sum(s.values())


def part2(raw: str):
    start, end, grid, lch, width, height = parse(raw)
    s = Counter()
    # debug_print_grid(lch)
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
    if raw == test1:
        return sum(c for k, c in s.items() if k >= 50)
    return sum(c for k, c in s.items() if k >= 100)


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

expected1 = sum(
    extract_ints(
        """
    There are 14 cheats that save 2 picoseconds.
    There are 14 cheats that save 4 picoseconds.
    There are 2 cheats that save 6 picoseconds.
    There are 4 cheats that save 8 picoseconds.
    There are 2 cheats that save 10 picoseconds.
    There are 3 cheats that save 12 picoseconds.
    There is one cheat that saves 20 picoseconds.
    There is one cheat that saves 36 picoseconds.
    There is one cheat that saves 38 picoseconds.
    There is one cheat that saves 40 picoseconds.
    There is one cheat that saves 64 picoseconds.
""".replace(
            "one", "1"
        )
    )[::2]
)

test2 = test1
expected2 = sum(
    extract_ints(
        """
    There are 32 cheats that save 50 picoseconds.
    There are 31 cheats that save 52 picoseconds.
    There are 29 cheats that save 54 picoseconds.
    There are 39 cheats that save 56 picoseconds.
    There are 25 cheats that save 58 picoseconds.
    There are 23 cheats that save 60 picoseconds.
    There are 20 cheats that save 62 picoseconds.
    There are 19 cheats that save 64 picoseconds.
    There are 12 cheats that save 66 picoseconds.
    There are 14 cheats that save 68 picoseconds.
    There are 12 cheats that save 70 picoseconds.
    There are 22 cheats that save 72 picoseconds.
    There are 4 cheats that save 74 picoseconds.
    There are 3 cheats that save 76 picoseconds.
"""
    )[::2]
)


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
