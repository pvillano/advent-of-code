from collections import defaultdict

from utils import benchmark, test
from utils.advent import get_input
from utils.graphs import reverse_edges
from utils.printing import debug_print


def preparse(raw):
    for line in raw.splitlines():
        prerequisite, dependent = (line
                                   .removeprefix("Step ")
                                   .removesuffix(" can begin.")
                                   .split(" must be finished before step "))
        yield dependent, prerequisite


# @degenerate
def parse(raw: str):
    """
    dicts remember insertion order,
    which is why I want to add entries
    in the order they will eventually be iterated.
    ...
    """
    precursors = defaultdict(list)
    for line in raw.splitlines():
        prerequisite, dependent = (line
                                   .removeprefix("Step ")
                                   .removesuffix(" can begin.")
                                   .split(" must be finished before step "))
        _ = precursors[prerequisite]
        precursors[dependent].append(prerequisite)
    return {k: v for k, v in sorted(precursors.items())}


def part1(raw: str):
    precursors = parse(raw)
    children = reverse_edges(precursors)
    seen = []
    while precursors:
        to_delete = False
        for k, v in precursors.items():
            if v:
                continue
            seen.append(k)
            for child in children[k]:
                precursors[child].remove(k)
            to_delete = k
            break
        if to_delete:
            del precursors[to_delete]
    return "".join(seen)


def part2(raw: str):
    if raw == test1:
        num_workers = 2
        def ttc(ch):
            return ord(ch) - ord('A') + 1
    else:
        num_workers = 5
        def ttc(ch):
            return ord(ch) - ord('A') + 61

    candidates = parse(raw)
    children = reverse_edges(candidates)
    current_time = 0
    wips = dict() # job name => finish time
    finishes_at = dict()
    while candidates or wips:
        # add as many jobs as you can
        to_delete = []
        for k, v in candidates.items():
            if len(wips) == num_workers:
                break
            if v:
                continue
            # room for k, enqueue
            wips[k] = current_time + ttc(k)
            to_delete.append(k)
        for k in to_delete:
            del candidates[k]
        # assert jobs are full or unmet dependencies

        debug_print(current_time, wips)

        # advance time
        next_time = min(wips.values())
        assert next_time >= current_time
        current_time = next_time
        for completed in list(k for k, v in wips.items() if v <= current_time):
            del wips[completed]
            for child in children[completed]:
                candidates[child].remove(completed)

        debug_print(current_time, wips)

    return current_time


test1 = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

expected1 = "CABDFE"

test2 = test1
expected2 = 15


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
