from collections import defaultdict
from itertools import combinations, count

from utils import benchmark, get_day, test


def parse(raw: str):
    atlas = defaultdict(list)
    lines = raw.splitlines()
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char != ".":
                atlas[char].append((r, c))
    return atlas, len(lines), len(lines[0])


def part1(raw: str):
    atlas, height, width = parse(raw)
    s = 0
    sparse = []
    for key, values in atlas.items():
        for first, second in combinations(values, 2):
            r1, c1 = first
            r2, c2 = second
            r3 = r1 + r1 - r2
            c3 = c1 + c1 - c2
            r4 = r2 + r2 - r1
            c4 = c2 + c2 - c1
            if r3 in range(height) and c3 in range(width):
                s += 1
                sparse.append((r3, c3))
            if r4 in range(height) and c4 in range(width):
                s += 1
                sparse.append((r4, c4))
    return len(set(sparse))


def part2(raw: str):
    atlas, height, width = parse(raw)
    sparse = set()
    for key, values in atlas.items():
        for first, second in combinations(values, 2):
            r1, c1 = first
            r2, c2 = second
            dr = r2 - r1
            dc = c2 - c1
            for i in count():
                r, c = r1 + i * dr, c1 + i * dc
                if r not in range(height) or c not in range(width):
                    break
                sparse.add((r, c))
            for i in count(0, -1):
                r, c = r1 + i * dr, c1 + i * dc
                if r not in range(height) or c not in range(width):
                    break
                sparse.add((r, c))
    return len(sparse)


test1 = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

expected1 = 14

test2 = test1
expected2 = 34


def main():
    test(part1, test1, expected1)
    raw = get_day(8)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
