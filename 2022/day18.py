from collections import deque
from itertools import product, chain, starmap

from utils import benchmark, get_day
from utils.itertools2 import rotations, transpose

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
    voxels = set(tuple(map(int, line.split(','))) for line in lines)
    sides = tuple(chain(rotations((1, 0, 0)), rotations((-1, 0, 0))))

    def neighbours(xyz):
        return [tuple(map(sum, zip(xyz, dxyz))) for dxyz in sides]

    def open_faces_count(xyz):
        return sum([x not in voxels for x in neighbours(xyz)])

    return sum(map(open_faces_count, voxels))


def part2():
    voxels = tuple(tuple(map(int, line.split(','))) for line in lines)

    mins = tuple(map(min, transpose(voxels)))
    maxes = tuple(map(max, transpose(voxels)))
    voxels = set(voxels)
    sides = tuple(chain(rotations((-1, 0, 0)), rotations((1, 0, 0))))

    def planify(i, bottom, top):
        if i == -1:
            return range(bottom, bottom + 1)
        if i == 0:
            return range(bottom, top + 1)
        if i == 1:
            return range(top, top + 1)

    planes = [tuple(starmap(planify, zip(x, mins, maxes))) for x in sides]

    outside = set()
    for plane in planes:
        for voxel in product(*plane):
            if voxel not in voxels:
                outside.add(voxel)
    todo = deque(outside)

    def neighbours(voxel):
        return [tuple(map(sum, zip(voxel, offset))) for offset in sides]

    def in_bounds(voxel):
        return all(starmap(lambda a, b, c: a <= b <= c, zip(mins, voxel, maxes)))

    explored = set()
    while todo:
        voxel = todo.pop()
        if voxel in explored:
            continue
        for neighbour in neighbours(voxel):
            if neighbour not in voxels and in_bounds(neighbour):
                outside.add(neighbour)
                todo.append(neighbour)
        explored.add(voxel)

    area = 0
    for voxel in product(*[range(start, stop + 1) for start, stop in zip(mins, maxes)]):
        if voxel in outside:
            continue
        for neighbour in neighbours(voxel):
            if not in_bounds(neighbour) or neighbour in outside:
                area += 1
    return area


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
