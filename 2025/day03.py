from utils import benchmark, test
from utils.advent import get_input, DEBUG
from utils.itertools2 import degenerate
from utils.printing import debug_print


@degenerate
def parse(raw: str):
    for line in raw.splitlines():
        yield list(map(int, line))


def part1(raw: str):
    total_joltage = 0
    for bank in parse(raw):
        largest_not_last = max(bank[:-1])
        idx_lnl = bank.index(largest_not_last)
        following_largest = max(bank[idx_lnl + 1:])
        total_joltage += largest_not_last * 10 + following_largest
    return total_joltage


def part2(raw: str):
    total_joltage = 0
    for bank in parse(raw):
        idx_prev_used = -1
        bank_joltage = 0
        for i in range(12):
            lnl = max(bank[idx_prev_used + 1:len(bank) - (12 - i - 1)])
            bank_joltage *= 10
            bank_joltage += lnl
            idx_prev_used = bank.index(lnl, idx_prev_used + 1)
        total_joltage += bank_joltage
    return total_joltage


test1 = """987654321111111
811111111111119
234234234234278
818181911112111
"""

expected1 = 357

test2 = test1
expected2 = 3121910778619


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
