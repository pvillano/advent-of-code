from itertools import product, count

from utils import benchmark, get_day, test
from utils.grids import rotate_clockwise
from utils.itertools2 import flatten


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret


def part1(raw: str):
    original_lines = parse(raw)
    cnt = 0

    for lines in [
        original_lines,
        rotate_clockwise(original_lines),
        rotate_clockwise(rotate_clockwise(original_lines)),
        rotate_clockwise(rotate_clockwise(rotate_clockwise(original_lines))),
    ]:
        for line in lines:
            for x, m, a, s in zip(line, line[1:], line[2:], line[3:]):
                if "".join((x, m, a, s)) == 'XMAS':
                    cnt += 1
        for diag_start in flatten([product(range(len(lines)), [0]), product([0], range(1, len(lines[0])))]):
            for dx in count():
                r0, c0 = diag_start
                r0 += dx
                c0 += dx
                try:
                    x, m, a, s = [lines[r0 + i][c0 + i] for i in range(4)]
                    if "".join((x, m, a, s)) == 'XMAS':
                        cnt += 1
                except IndexError:
                    break
    return cnt


def part2(raw: str):
    original_lines = parse(raw)
    cnt = 0

    for lines in [
        original_lines,
        rotate_clockwise(original_lines),
        rotate_clockwise(rotate_clockwise(original_lines)),
        rotate_clockwise(rotate_clockwise(rotate_clockwise(original_lines))),
    ]:
        for r0, c0 in product(range(len(lines) - 2), range(len(lines[0]) - 2)):
            msams = ""
            for dr, dc in [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]:
                r, c = r0 + dr, c0 + dc
                msams += lines[r][c]
            if msams == "MSAMS":
                cnt += 1
    return cnt


test1 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

expected1 = 18

test2 = test1
expected2 = 9


def main():
    test(part1, test1, expected1)
    raw = get_day(4)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
