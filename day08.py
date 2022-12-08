from itertools import count, product

from utils import benchmark, get_day

test = """30373
25512
65332
33549
35390"""

raw = get_day(8, test)
lines = raw.split("\n")


def part1():
    data = [list(map(int, line)) for line in lines]
    rows = len(data)
    cols = len(data[0])
    visible = [[False] * cols for _ in range(rows)]
    index_sets = (
        [[(i, j) for i in range(rows)] for j in range(cols)]
        + [[(i, j) for i in reversed(range(rows))] for j in range(cols)]
        + [[(i, j) for j in range(cols)] for i in range(rows)]
        + [[(i, j) for j in reversed(range(cols))] for i in range(rows)]
    )
    for index_set in index_sets:
        highest_seen = -1
        for i, j in index_set:
            if data[i][j] > highest_seen:
                highest_seen = data[i][j]
                visible[i][j] = True

    return sum(map(sum, visible))


def part2():
    data = [list(map(int, line)) for line in lines]
    rows = len(data)
    cols = len(data[0])

    def generator():
        for i, j in product(range(rows), range(cols)):
            highest_allowed = data[i][j]
            score = 1
            for d_i, d_j in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                visible_cnt = 0
                for k in count(1):
                    i2, j2 = i + k * d_i, j + k * d_j
                    if not (i2 in range(rows) and j2 in range(cols)):
                        break
                    visible_cnt += 1
                    if data[i2][j2] >= highest_allowed:
                        break
                score *= visible_cnt
            yield score

    return max(generator())


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
