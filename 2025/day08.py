import operator
from functools import reduce
from heapq import heapify, heappop
from itertools import starmap

from black.trans import defaultdict

from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate
from utils.parsing import extract_ints


@degenerate
def parse(raw: str):
    return map(extract_ints, raw.splitlines())


def l2squared(a, b):
    return sum(starmap(lambda aa, bb: (aa - bb) ** 2, zip(a, b)))


def part1(raw: str):
    if raw == test1:
        n_edges = 10
    else:
        n_edges = 1000
    coords_list = parse(raw)
    adjacency = defaultdict(list)
    edge_heap = []
    # heapify()
    for abc in coords_list:
        for xyz in coords_list:
            if xyz <= abc:  # remove self and duplicates
                continue
            edge_heap.append((l2squared(xyz, abc), abc, xyz))
    heapify(edge_heap)
    for _ in range(n_edges):
        _, abc, xyz = heappop(edge_heap)
        adjacency[abc].append(xyz)
        adjacency[xyz].append(abc)
    seen = set()
    connected_component_list = []
    for abc in coords_list:
        connected_component = 0
        stack = [abc]
        while stack:
            xyz = stack.pop()
            if xyz in seen:
                continue
            for ghi in adjacency[xyz]:
                if ghi in seen:
                    continue
                stack.append(ghi)

            # these two always together
            seen.add(xyz)
            connected_component += 1
        connected_component_list.append(connected_component)
    connected_component_list.sort(reverse=True)
    return reduce(operator.mul, connected_component_list[:3])


class UnionFind[T]:
    toIndex: dict[T, int]
    pointers: list[int]
    ranks: list[int]

    def __init__(self, items: list[T]):
        self.toIndex = {item: i for i, item in enumerate(items)}
        self.pointers = list(range(len(items)))
        self.setCount = len(items)
        self.ranks = [0] * len(items)

    def find(self, x: int) -> int:
        while self.pointers[x] != x:
            x, self.pointers[x] = self.pointers[x], self.pointers[self.pointers[x]]
        return x

    def union(self, x_original: T, y_original: T) -> None:
        x = self.toIndex[x_original]
        y = self.toIndex[y_original]
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.ranks[x] < self.ranks[y]:
            x, y = y, x
        self.pointers[y] = x
        self.setCount -= 1
        if self.ranks[x] == self.ranks[y]:
            self.ranks[x] += 1
        return


def part2(raw: str):
    if raw == test1:
        n_edges = 10
    else:
        n_edges = 1000
    coords_list = parse(raw)
    adjacency = defaultdict(list)
    edge_heap = []
    # heapify()
    for abc in coords_list:
        for xyz in coords_list:
            if xyz <= abc:  # remove self and duplicates
                continue
            edge_heap.append((l2squared(xyz, abc), abc, xyz))
    heapify(edge_heap)
    unionFind = UnionFind(coords_list)
    while unionFind.setCount > 1:
        _, abc, xyz = heappop(edge_heap)
        unionFind.union(abc, xyz)
    return abc[0] * xyz[0]


test1 = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

expected1 = 40

test2 = test1
expected2 = None


def main():
    raw = get_input(__file__)

    test(part1, test1, expected1)
    benchmark(part1, raw)

    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
