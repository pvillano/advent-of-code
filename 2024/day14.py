from itertools import count

from utils import benchmark, get_day, test
from utils.grids import NEWS_XY
from utils.parsing import extract_ints
from utils.printing import debug_print, debug_print_sparse_grid


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        px, py, vx, vy = extract_ints(line)
        ret.append((px, py, vx, vy))
    return ret


def part1(raw: str):
    lines = parse(raw)
    width, height = 101, 103
    quads = [[0, 0], [0, 0]]
    if raw == test1:
        width, height = 11, 7
    for px, py, vx, vy in lines:
        x = (px + vx * 100) % width
        y = (py + vy * 100) % height
        if x == width // 2 or y == height // 2:
            continue
        quads[x > width // 2][y > height // 2] += 1
    return quads[0][0] * quads[0][1] * quads[1][0] * quads[1][1]


def part2(raw: str):
    lines = parse(raw)
    width, height = 101, 103
    best_lonelies = len(lines)
    best_t = 0
    for t in range(width * height):
        positions = {((px + vx * t) % width, (py + vy * t) % height): "#" for px, py, vx, vy in lines}
        lonelies = 0
        for x, y in positions:
            friend = False
            for dx, dy in NEWS_XY:
                if (x + dx, y + dy) in positions:
                    friend = True
                    continue
            if not friend:
                lonelies += 1
        if lonelies < best_lonelies:
            best_lonelies = lonelies
            best_t = t
    return best_t


test1 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

expected1 = 12

test2 = test1
expected2 = None


def main():
    test(part1, test1, expected1)
    raw = get_day(14)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
