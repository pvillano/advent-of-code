from collections import deque
from itertools import product
from math import inf

from utils import benchmark, debug_print, get_day

test = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

raw = get_day(12, test)
lines = raw.split("\n")


def part1():
    row_count = len(lines)
    col_count = len(lines[0])
    start = None
    end = None
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == "S":
                start = (row, col)
            if c == "E":
                end = (row, col)

    data = [list(map(lambda x: ord(x), line)) for line in lines]
    data[start[0]][start[1]] = ord('a')
    data[end[0]][end[1]] = ord('z')

    debug_print(data)
    distances = [[inf] * col_count for _ in range(row_count)]
    distances[start[0]][start[1]] = 0
    todo = deque()
    todo.appendleft(start)
    while todo:
        r, c = todo.pop()
        for dr, dc in ((1, 0), (0, -1), (-1, 0), (0, 1)):
            r2, c2 = r + dr, c + dc
            if r2 in range(row_count) and c2 in range(col_count) and data[r2][c2] - data[r][c] < 2:
                if distances[r2][c2] > distances[r][c] + 1:
                    distances[r2][c2] = distances[r][c] + 1
                    todo.append((r2, c2))
    return distances[end[0]][end[1]]


def part2():
    row_count = len(lines)
    col_count = len(lines[0])
    start = None
    end = None
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == "S":
                start = (row, col)
            if c == "E":
                end = (row, col)

    data = [list(map(lambda x: ord(x), line)) for line in lines]
    data[start[0]][start[1]] = ord('a')
    data[end[0]][end[1]] = ord('z')

    debug_print(data)
    distances = [[inf] * col_count for _ in range(row_count)]
    distances[end[0]][end[1]] = 0
    todo = deque()
    todo.appendleft(end)
    while todo:
        r, c = todo.pop()
        for dr, dc in ((1, 0), (0, -1), (-1, 0), (0, 1)):
            r2, c2 = r + dr, c + dc
            if r2 in range(row_count) and c2 in range(col_count) and data[r][c] - data[r2][c2] < 2:
                if distances[r2][c2] > distances[r][c] + 1:
                    distances[r2][c2] = distances[r][c] + 1
                    todo.append((r2, c2))

    def gen():
        for row, col in product(range(row_count), range(col_count)):
            if data[row][col] == ord('a') and distances[row][col] != inf:
                yield distances[row][col]

    return min(gen())


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
