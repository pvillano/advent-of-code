from copy import deepcopy

from tqdm import tqdm

from utils import benchmark, get_day, test
from utils.printing import debug_print_grid, debug_print


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret


def part1(raw: str):
    lines = parse(raw)
    seen = [[0] * len(lines[0]) for i in range(len(lines))]
    r, c = -1, -1
    for idx, row in enumerate(lines):
        tmp = row.find('^')
        if tmp != -1:
            r, c = idx, tmp
    facing = 0
    NESW_RC = ((-1, 0), (0, 1), (1, 0), (0, -1))

    while 0 <= r < len(lines) and 0 <= c < len(lines[0]):
        seen[r][c] = 1
        nr, nc = r + NESW_RC[facing][0], c + NESW_RC[facing][1]
        if nr not in range(len(lines)) or nc not in range(len(lines[0])):
            return sum(map(sum, seen))
        while lines[nr][nc] == '#':
            facing = (facing + 1) % 4
            nr, nc = r + NESW_RC[facing][0], c + NESW_RC[facing][1]
            if nr not in range(len(lines)) or nc not in range(len(lines[0])):
                return sum(map(sum, seen))
        r, c = nr, nc

        debug_print_grid(seen)
        debug_print()


def part2(raw: str):
    s = 0
    lines = parse(raw)
    r, c = -1, -1
    for idx, row in enumerate(lines):
        tmp = row.find('^')
        if tmp != -1:
            r, c = idx, tmp
    lines = [list(l) for l in raw.splitlines()]
    for i in tqdm(range(len(lines))):
        for j in range(len(lines[0])):
            if lines[i][j] != '.':
                continue
            new_lines = deepcopy(lines)
            new_lines[i][j] = '#'
            if loops(new_lines, r, c):
                s += 1
    return s


def loops(lines, r, c):
    seen = [[set() for j in range(len(lines[0]))] for i in range(len(lines))]
    facing = 0
    NESW_RC = ((-1, 0), (0, 1), (1, 0), (0, -1))

    while 0 <= r < len(lines) and 0 <= c < len(lines[0]):
        if facing in seen[r][c]:
            return True
        seen[r][c].add(facing)
        nr, nc = r + NESW_RC[facing][0], c + NESW_RC[facing][1]
        if nr not in range(len(lines)) or nc not in range(len(lines[0])):
            return False
        while lines[nr][nc] == '#':
            facing = (facing + 1) % 4
            nr, nc = r + NESW_RC[facing][0], c + NESW_RC[facing][1]
            if nr not in range(len(lines)) or nc not in range(len(lines[0])):
                return False
        r, c = nr, nc
    return False


test1 = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

expected1 = 41

test2 = test1
expected2 = 6


def main():
    test(part1, test1, expected1)
    raw = get_day(6)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
