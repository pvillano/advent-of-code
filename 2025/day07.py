from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate


@degenerate
def parse(raw: str):
    s_row, *rest = raw.strip().splitlines()
    return s_row.index('S'), rest


def part1(raw: str):
    s_index, atlas = parse(raw)
    beams = [False] * len(atlas[0])
    beams[s_index] = True
    split_count = 0
    for row in atlas:
        next_beams = [False for _ in atlas[0]]
        for i in range(len(beams)):
            # scatter not gather
            if not beams[i]:
                continue
            if row[i] == '.':
                next_beams[i] = True
                continue
            split_count += 1
            next_beams[i - 1] = True
            next_beams[i + 1] = True
        beams = next_beams
    return split_count


def part2(raw: str):
    s_index, atlas = parse(raw)
    superpositions = [0] * len(atlas[0])
    superpositions[s_index] = 1
    for row in atlas[1:]:
        next_superpositions = [0 for _ in atlas[0]]
        for i in range(len(superpositions)):
            # scatter not gather
            if not superpositions[i]:
                continue
            if row[i] == '.':
                next_superpositions[i] += superpositions[i]
                continue
            next_superpositions[i - 1] += superpositions[i]
            next_superpositions[i + 1] += superpositions[i]
        superpositions = next_superpositions
    return sum(superpositions)


test1 = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

expected1 = 21

test2 = test1
expected2 = 40


def main():
    raw = get_input(__file__)

    test(part1, test1, expected1)
    benchmark(part1, raw)

    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
