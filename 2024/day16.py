from collections import deque
from math import inf

from utils import benchmark, get_input, test
from utils.grids import NESW_RC, grid_index
from utils.printing import debug_print


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append([l for l in line])
    return ret


def lch(raw: str):
    lines = parse(raw)
    height, width = len(lines), len(lines[0])
    start_r, start_c = grid_index(lines, "S")
    end_r, end_c = grid_index(lines, "E")

    least_cost_here = [[[inf] * 4 for _ in range(width)] for _ in range(height)]
    least_cost_here[start_r][start_c][1] = 0
    q = deque([(start_r, start_c, 1)])
    while q:
        # for each neighbour if you give a better cost, lower the cost, add to the queue
        r, c, facing = q.pop()
        if r == end_r and c == end_c:
            debug_print(min(least_cost_here[r][c]))
        cost_here = least_cost_here[r][c][facing]
        for new_facing in range(4):
            d_facing = abs(facing - new_facing)
            d_facing = min(d_facing, 4 - d_facing)
            new_cost = cost_here + 1000 * d_facing
            if least_cost_here[r][c][new_facing] > new_cost:
                least_cost_here[r][c][new_facing] = new_cost
                q.appendleft((r, c, new_facing))
        dr, dc = NESW_RC[facing]
        r += dr
        c += dc
        if lines[r][c] == "#":
            continue
        new_cost = cost_here + 1
        if least_cost_here[r][c][facing] > new_cost:
            least_cost_here[r][c][facing] = new_cost
            q.appendleft((r, c, facing))
    return least_cost_here, start_r, start_c, end_r, end_c


def part1(raw):
    least_cost_here, start_r, start_c, end_r, end_c = lch(raw)
    return min(least_cost_here[end_r][end_c])


def part2(raw: str):
    least_cost_here, start_r, start_c, end_r, end_c = lch(raw)
    height, width = len(least_cost_here), len(least_cost_here[0])
    end_facings = [i for i in range(4) if least_cost_here[end_r][end_c][i] == min(least_cost_here[end_r][end_c])]
    q = deque([(end_r, end_c, facing) for facing in end_facings])
    progeny = [[[False] * 4 for _ in range(width)] for _ in range(height)]
    for f in end_facings:
        progeny[end_r][end_c][f] = True
    while q:
        r, c, facing = q.pop()
        cost_here = least_cost_here[r][c][facing]
        assert cost_here != inf
        for new_facing in range(4):
            if progeny[r][c][new_facing]:
                continue
            d_facing = abs(facing - new_facing)
            d_facing = min(d_facing, 4 - d_facing)
            new_cost = cost_here - 1000 * d_facing
            if least_cost_here[r][c][new_facing] == new_cost:
                progeny[r][c][new_facing] = True
                q.appendleft((r, c, new_facing))
        dr, dc = NESW_RC[facing]
        r -= dr
        c -= dc
        if least_cost_here[r][c][facing] == cost_here - 1:
            progeny[r][c][facing] = True
            q.appendleft((r, c, facing))
    s = 0
    for row in progeny:
        s += sum(map(any, row))
    return s


test1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

expected1 = 7036

test2 = test1
expected2 = 45


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
