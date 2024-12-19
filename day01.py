from collections import Counter

from utils import benchmark, get_day, test
from utils.grids import transpose
from utils.parsing import extract_ints


def parse(raw: str):
    return list(map(extract_ints, raw.splitlines()))


def part1(raw: str):
    left_list, right_list = map(sorted, transpose(parse(raw)))
    return sum([abs(left - right) for left, right in zip(left_list, right_list)])


def part2(raw: str):
    left_list, right_list = map(sorted, transpose(parse(raw)))
    counts = Counter(right_list)
    return sum(left * counts[left] for left in left_list)


test1 = """3   4
4   3
2   5
1   3
3   9
3   3"""

expected1 = 11

test2 = test1
expected2 = 31


def main():
    test(part1, test1, expected1)
    raw = get_day(1)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
