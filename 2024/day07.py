from tqdm import tqdm

from utils import benchmark, get_day, test
from utils.parsing import extract_ints


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(extract_ints(line))
    return ret


def dfs(target, current, remaining):
    if target == current and not remaining:
        return True
    if current > target:
        return False
    if not remaining:
        return False
    if dfs(target, current * remaining[0], remaining[1:]):
        return True
    if dfs(target, current + remaining[0], remaining[1:]):
        return True
    return False


def part1(raw: str):
    lines = parse(raw)
    s = 0
    for target, *rest in tqdm(lines):
        if dfs(target, rest[0], rest[1:]):
            s += target
    return s


def dfs2(target, current, remaining):
    if target == current and not remaining:
        return True
    if current > target:
        return False
    if not remaining:
        return False
    head, *rest = remaining
    if dfs2(target, int(f"{current}{head}"), rest):
        return True
    if dfs2(target, current * head, rest):
        return True
    if dfs2(target, current + head, rest):
        return True
    return False


def part2(raw: str):
    lines = parse(raw)
    s = 0
    # for target, *rest in tqdm(lines):
    for target, *rest in lines:
        if dfs2(target, rest[0], rest[1:]):
            s += target
    return s


test1 = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

expected1 = 3749

test2 = test1
expected2 = 11387


def main():
    # test(part1, test1, expected1)
    raw = get_day(7)
    # benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
# 426214137279934
# 426214137279934
# 426214137279934
# 3602464018775
