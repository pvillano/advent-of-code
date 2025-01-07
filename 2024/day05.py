from collections import defaultdict

from utils import benchmark, get_day, test
from utils.parsing import extract_ints


def parse(raw: str):
    first, second = raw.split("\n\n")
    rule_pairs = [extract_ints(line) for line in first.splitlines()]
    rules = defaultdict(set)
    for before, after in rule_pairs:
        rules[before].add(after)

    updates = [extract_ints(line) for line in second.splitlines()]
    return rules, updates


def part1(raw: str):
    rules, updates = parse(raw)
    s = 0
    for up in updates:
        failed = False
        for idx, page in enumerate(up):
            if rules[page].intersection(up[:idx]):
                failed = True
                break
        if not failed:
            s += up[(len(up) - 1) // 2]
    return s


def part2(raw: str):
    rules, updates = parse(raw)
    s = 0
    for up in updates:
        up = list(up)
        failed = False
        for idx, page in enumerate(up):
            if rules[page].intersection(up[:idx]):
                failed = True
                break
        if failed:
            for i in range(len(up)):
                for j in range(i + 1, len(up)):
                    if up[i] in rules[up[j]]:
                        up[i], up[j] = up[j], up[i]
            s += up[(len(up) - 1) // 2]
    return s


test1 = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

expected1 = 143

test2 = test1
expected2 = 123


def main():
    test(part1, test1, expected1)
    raw = get_day(5)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
