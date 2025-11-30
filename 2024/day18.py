from collections import deque
from math import inf

from utils import benchmark, get_input, test
from utils.grids import NESW_RC
from utils.parsing import extract_ints


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(extract_ints(line))
    return ret


def part1(raw: str):
    sparse = parse(raw)
    if raw == test1:
        w = 6
        l = 12
    else:
        w = 70
        l = 1024
    return costs(sparse[:l], w)


def costs(sparse, w):
    dense = [[True] * (w + 1) for _ in range(w + 1)]
    lch = [[inf] * (w + 1) for _ in range(w + 1)]
    lch[0][0] = 0

    for c, r in sparse:
        dense[r][c] = False
    q = deque([(0, 0)])
    while q:
        r, c = q.pop()
        cost_here = lch[r][c]
        for dr, dc in NESW_RC:
            rr, cc = r + dr, c + dc
            if rr not in range(w + 1) or cc not in range(w + 1):
                continue
            if not dense[rr][cc]:
                continue
            if lch[rr][cc] > cost_here + 1:
                lch[rr][cc] = cost_here + 1
                q.appendleft((rr, cc))
    return lch[w][w]


def part2(raw: str):
    sparse = parse(raw)
    if raw == test1:
        w = 6
    else:
        w = 70
    before = 0
    after = len(sparse)
    while after - before > 1:
        t_avg = (before + after) // 2
        if costs(sparse[:t_avg], w) == inf:
            after = t_avg
        else:
            before = t_avg
    return sparse[after - 1]


test1 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

expected1 = 22

test2 = test1
expected2 = (6, 1)


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
