from itertools import starmap

from utils import benchmark, get_day, test
from utils.grids import NESW_RC


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(list(map(int, line)))
    return ret


def part1(raw: str):
    atlas = parse(raw)
    height = len(atlas)
    width = len(atlas[0])
    trailheads = []
    for r, row in enumerate(atlas):
        for c, topo in enumerate(row):
            if topo == 0:
                trailheads.append((r, c))

    def score(head):
        head_r, head_c = head
        assert atlas[head_r][head_c] == 0
        ancestors = {(head_r, head_c)}
        for generation in range(9):
            new_ancestors = []
            for r1, c1 in ancestors:
                for dr, dc in NESW_RC:
                    r2, c2 = r1 + dr, c1 + dc
                    if r2 in range(height) and c2 in range(width) and atlas[r2][c2] == generation + 1:
                        new_ancestors.append((r2, c2))
            ancestors = set(new_ancestors)
        return len(ancestors)

    return sum(map(score, trailheads))


def part2(raw: str):
    atlas = parse(raw)
    height = len(atlas)
    width = len(atlas[0])
    trailheads = []
    for r, row in enumerate(atlas):
        for c, topo in enumerate(row):
            if topo == 0:
                trailheads.append((r, c, 0))

    def score(r1, c1, generation):
        if generation == 9:
            return 1
        s = 0
        for dr, dc in NESW_RC:
            r2, c2 = r1 + dr, c1 + dc
            if r2 in range(height) and c2 in range(width) and atlas[r2][c2] == generation + 1:
                s += score(r2, c2, generation + 1)
        return s

    return sum(starmap(score, trailheads))


test1 = """0123
1234
8765
9876
"""

expected1 = 1

test11 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

expected11 = 36

test2 = test11
expected2 = 81


def main():
    test(part1, test1, expected1)
    test(part1, test11, expected11)
    raw = get_day(10)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
