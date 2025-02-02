from collections import defaultdict

from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate


@degenerate
def parse(raw: str):
    precursors = defaultdict(list)
    for line in raw:
        prerequisite, dependent = (line
                                   .removeprefix("Step ")
                                   .removesuffix(" can begin.")
                                   .split(" must be finished before step "))
        _ = precursors[prerequisite]
        precursors[dependent].append(prerequisite)
    return precursors


def part1(raw: str):
    precursors = parse(raw)




def part2(raw: str):
    parse(raw)


test1 = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

expected1 = "CABDFE"

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
