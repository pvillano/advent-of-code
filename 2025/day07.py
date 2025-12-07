from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate


@degenerate
def parse(raw: str):
    return raw.strip().splitlines()


def part1(raw: str):
    atlas = parse(raw)
    beam_here = [False for _ in atlas[0]]
    beam_here[atlas[0].index('S')] = True
    split_count = 0
    for row in atlas[1:]:
        next_beam = [False for _ in atlas[0]]
        for i in range(len(beam_here)):
            # scatter not gather
            if not beam_here[i]:
                continue
            if row[i] == '.':
                next_beam[i] = True
                continue
            assert row[i] == '^'
            split_count += 1
            if i - 1 >= 0:
                next_beam[i - 1] = True
                next_beam[i + 1] = True
        beam_here = next_beam
    return split_count


def part2(raw: str):
    atlas = parse(raw)
    timeline_count = [0 for _ in atlas[0]]
    timeline_count[atlas[0].index('S')] = 1
    for row in atlas[1:]:
        next_beam = [False for _ in atlas[0]]
        for i in range(len(timeline_count)):
            # scatter not gather
            if not timeline_count[i]:
                continue
            if row[i] == '.':
                next_beam[i] += timeline_count[i]
                continue
            assert row[i] == '^'
            if i - 1 >= 0:
                next_beam[i - 1] += timeline_count[i]
                next_beam[i + 1] += timeline_count[i]
        timeline_count = next_beam
    return sum(timeline_count)


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
