import trio

from utils.parallel import parallel_map
from utils import benchmark, get_day, test


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

def seener(raw: str):
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
            return seen
        while lines[nr][nc] == '#':
            facing = (facing + 1) % 4
            nr, nc = r + NESW_RC[facing][0], c + NESW_RC[facing][1]
            if nr not in range(len(lines)) or nc not in range(len(lines[0])):
                return seen
        r, c = nr, nc


def part2(raw: str):
    seen = seener(raw)
    s = 0
    lines = raw.splitlines()
    rows, columns = len(lines), len(lines[0])
    r, c = -1, -1
    for idx, row in enumerate(lines):
        tmp = row.find('^')
        if tmp != -1:
            r, c = idx, tmp
    # for i in tqdm(range(len(lines))):
    for i in range(rows):
        for j in range(columns):
            if lines[i][j] != '.':
                continue
            if not seen[i][j]:
                continue
            new_lines = lines[:]
            new_lines[i] =  lines[i][:j] + '#' + lines[i][j+1:]
            if loops(new_lines, r, c):
                s += 1
    return s

def part2parallel(raw: str):
    seen = seener(raw)
    lines = parse(raw)
    rows, columns = len(lines), len(lines[0])
    r, c = -1, -1
    for idx, row in enumerate(lines):
        tmp = row.find('^')
        if tmp != -1:
            r, c = idx, tmp
    inputs = []
    for i in range(rows):
        for j in range(columns):
            if lines[i][j] != '.':
                continue
            if not seen[i][j]:
                continue
            new_lines = lines[:]
            new_lines[i] =  lines[i][:j] + '#' + lines[i][j+1:]
            inputs.append([new_lines,r,c])

    return sum(trio.run(parallel_map, loops, inputs))

def loops(lines, r, c):
    rows, columns = len(lines), len(lines[0])
    seen = [[0 for j in range(columns)] for i in range(rows)]
    facing = 0
    NESW_RC = ((-1, 0), (0, 1), (1, 0), (0, -1))

    while 0 <= r < rows and 0 <= c < columns:
        if (1 << facing) & seen[r][c]:
            return True
        seen[r][c] |= 1 << facing
        nr, nc = r + NESW_RC[facing][0], c + NESW_RC[facing][1]
        if nr not in range(rows) or nc not in range(columns):
            return False
        while lines[nr][nc] == '#':
            facing = (facing + 1) % 4
            nr, nc = r + NESW_RC[facing][0], c + NESW_RC[facing][1]
            if nr not in range(rows) or nc not in range(columns):
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
    test(part2parallel, test2, expected2)
    benchmark(part2parallel, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()

"""
Testing part1 01:00AM
Passed in 0.000 seconds

Started part1 01:00AM
5080
Completed in 0.002 seconds.

Testing part2parallel 01:00AM
Passed in 2.127 seconds

Started part2parallel 01:00AM
1919
Completed in 3.063 seconds.

Testing part2 01:00AM
Passed in 0.001 seconds

Started part2 01:00AM
1919
Completed in 5.825 seconds.
"""