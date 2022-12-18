import operator
from collections import defaultdict, deque, Counter
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, reduce
from itertools import (
    accumulate,
    count,
    cycle,
    product,
    permutations,
    combinations,
    pairwise,
)
from math import sqrt, floor, ceil, gcd, sin, cos, atan2

from otqdm import otqdm

from utils import benchmark, debug_print, debug_print_grid, debug_print_sparse_grid, get_day, pipe, DEBUG

test = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

raw = get_day(18, test)
lines = raw.split("\n")


def part1():
    voxes = [tuple(map(int, line.split(','))) for line in lines]
    sides = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    )
    voxes = set(voxes)
    tot = 0
    # debug_print(voxes)
    for x, y, z in voxes:
        for dx, dy, dz in sides:
            xx, yy, zz = x + dx, y + dy, z + dz
            if (xx, yy, zz) not in voxes:
                tot += 1
    return tot


def part2():
    voxes = [tuple(map(int, line.split(','))) for line in lines]

    transposed = [[voxes[j][i] for j in range(len(voxes))] for i in range(3)]
    mins = list(map(min, transposed))
    maxes = list(map(max, transposed))
    sides = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
    )

    voxes_set = set(voxes)
    outside = set()
    explored = set()

    assert tuple(mins) not in voxes_set
    todo = deque()
    for l1, l2, l3 in product(*[(range(mins[i], maxes[i] + 1), (mins[i], maxes[i] + 1)) for i in range(3)]):
        if isinstance(l1, range) and isinstance(l2, range) and isinstance(l3, range):
            continue
        for x, y, z in product(l1, l2, l3):
            if (x, y, z) not in voxes_set and (x, y, z) not in outside:
                outside.add((x, y, z))
                todo.append((x, y, z))
    while todo:
        x, y, z = todo.pop()
        if (x, y, z) in explored:
            continue
        for dx, dy, dz in sides:
            xx, yy, zz = x + dx, y + dy, z + dz
            if ((xx, yy, zz) not in voxes_set
                    and xx in range(mins[0], maxes[0] + 1)
                    and yy in range(mins[1], maxes[1] + 1)
                    and zz in range(mins[2], maxes[2] + 1)):
                outside.add((xx, yy, zz))
                todo.append((xx, yy, zz))
        explored.add((x, y, z))

    if DEBUG:
        assert (2, 2, 5) not in outside

    area = 0
    cube_count = 0
    for x in range(mins[0], maxes[0] + 1):
        for y in range(mins[1], maxes[1] + 1):
            for z in range(mins[2], maxes[2] + 1):
                if (x, y, z) in outside:
                    continue
                for dx, dy, dz in sides:
                    xx, yy, zz = x + dx, y + dy, z + dz
                    if (xx not in range(mins[0], maxes[0] + 1)
                            or yy not in range(mins[1], maxes[1] + 1)
                            or zz not in range(mins[2], maxes[2] + 1)
                            or (xx, yy, zz) in outside):
                        area += 1
    return area


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
