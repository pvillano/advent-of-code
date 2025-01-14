from collections import Counter
from itertools import product, chain

from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate
from utils.parsing import extract_ints

import numpy as np

from utils.printing import debug_print_grid, debug_print


@degenerate
def parse(raw: str):
    for line in raw.splitlines():
        yield extract_ints(line)

azAZ = "".join(map(chr, range(ord('a'), ord('z') + 1))) + "".join(map(chr, range(ord('A'), ord('Z') + 1)))

def part1(raw: str):
    coords = parse(raw)
    max_x = max(x for x, _ in coords)
    min_x = min(x for x, _ in coords)
    max_y = max(y for _, y in coords)
    min_y = min(y for _, y in coords)
    assert min_x > 0 and min_y > 0
    grid = np.full((max_x + 1, max_y + 1), " ", np.character)
    for i, (x, y) in enumerate(coords):
        grid[x,y] = azAZ[i] # somewhat gracefully handle 52

    def vn_hood(x, y):
        if x > 0:
            yield x - 1, y
        if y > 0:
            yield x, y - 1
        if x < max_x:
            yield x + 1, y
        if y < max_y:
            yield x, y + 1

    for generation in range(max(max_x, max_y)):
        changed = False
        new_grid = grid.copy()
        for x, y in product(range(max_x + 1), range(max_y + 1)):
            ch = grid[x, y]
            if ch != b' ':
                continue
            neighbours = set(grid[x1, y1] for x1, y1 in vn_hood(x, y))
            interesting_neighbours = neighbours - {b" "}
            if len(interesting_neighbours) == 0:
                continue
            changed = True
            if len(interesting_neighbours) == 1:
                new_grid[x,y] = next(iter(interesting_neighbours))
            else:
                new_grid[x,y] = '.'
        grid = new_grid
        debug_print("\n".join(b''.join(row).decode("utf-8") for  row in grid.transpose()))
        debug_print("-" * grid.shape[1])
        if not changed:
            break
    boundry_bois = set(chain(grid[0], grid[-1], grid[:, 0], grid[:, -1]))
    counts = Counter(grid.flatten())
    for ch, count in counts.most_common():
        if ch not in boundry_bois:
            return count
    pass



def part2(raw: str):
    parse(raw)


test1 = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

expected1 = 17

test2 = test1
expected2 = None


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
