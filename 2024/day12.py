from itertools import groupby

from utils import benchmark, get_input, test
from utils.grids import NEWS_RC
from utils.printing import debug_print


def parse(raw: str):
    return raw.splitlines()


def part1(raw: str):
    lines = parse(raw)
    height, width = len(lines), len(lines[0])
    seen = [[False] * width for _ in range(height)]
    total_price = 0
    for start_r in range(height):
        for start_c in range(width):
            if seen[start_r][start_c]:
                continue
            ch = lines[start_r][start_c]
            region = []

            def recurse(r, c):
                nonlocal perimeter
                if r not in range(height) or c not in range(width):
                    return
                if seen[r][c]:
                    return
                if lines[r][c] != ch:
                    return
                region.append((r, c))
                seen[r][c] = True
                for dr, dc in NEWS_RC:
                    nr, nc = r + dr, c + dc
                    recurse(nr, nc)

            recurse(start_r, start_c)
            area = len(region)

            perimeter = 0
            for r, c in region:
                for dr, dc in NEWS_RC:
                    nr, nc = r + dr, c + dc
                    if nr not in range(height) or nc not in range(width) or lines[nr][nc] != ch:
                        # print(nr, nc)
                        perimeter += 1

            debug_print("ch", ch, "area", area, "perimeter", perimeter)
            total_price += area * perimeter
    return total_price


def part2(raw: str):
    lines = parse(raw)
    height, width = len(lines), len(lines[0])
    seen = [[False] * width for _ in range(height)]
    total_price = 0
    for start_r in range(height):
        for start_c in range(width):
            if seen[start_r][start_c]:
                continue
            ch = lines[start_r][start_c]
            region = []

            def recurse(r, c):
                if r not in range(height) or c not in range(width):
                    return
                if seen[r][c]:
                    return
                if lines[r][c] != ch:
                    return
                region.append((r, c))
                seen[r][c] = True
                for dr, dc in NEWS_RC:
                    nr, nc = r + dr, c + dc
                    recurse(nr, nc)

            recurse(start_r, start_c)
            area = len(region)

            perimeters = []
            for r, c in region:
                for news, (dr, dc) in zip("NEWS", NEWS_RC):
                    nr, nc = r + dr, c + dc
                    if nr not in range(height) or nc not in range(width) or lines[nr][nc] != ch:
                        perimeters.append((nr, nc, news))
            key = lambda x: x[2]  # facing
            perimeters.sort(key=key)
            perimeter = 0
            for news_id, group in groupby(perimeters, key):
                group = list(group)
                if news_id in "NS":
                    group.sort(key=lambda x: x[0])
                    for r, group2 in groupby(group, key=lambda x: x[0]):
                        group2 = list(group2)
                        group2.sort()
                        prev_c = -999
                        for _, c, _ in group2:
                            if c != prev_c + 1:
                                perimeter += 1
                            prev_c = c
                else:
                    assert news_id in "EW"
                    group.sort(key=lambda x: x[1])
                    for c, group2 in groupby(group, key=lambda x: x[1]):
                        group2 = list(group2)
                        group2.sort()
                        prev_r = -999
                        for r, _, _ in group2:
                            if r != prev_r + 1:
                                perimeter += 1
                            prev_r = r
            cost = area * perimeter
            debug_print("ch", ch, "area", area, "perimeter", perimeter, "cost", cost)
            total_price += cost
    return total_price


test1 = """AAAA
BBCD
BBCC
EEEC"""

expected1 = 140

test11 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

expected11 = 772

test12 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

expected12 = 1930

test2 = test1
expected2 = 80
test21 = test11
expected21 = 436
test22 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
expected22 = 236
test23 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
expected23 = 368


def main():
    test(part1, test1, expected1)
    test(part1, test11, expected11)
    test(part1, test12, expected12)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    test(part2, test21, expected21)
    test(part2, test22, expected22)
    test(part2, test23, expected23)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
