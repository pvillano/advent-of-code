from collections import deque, defaultdict

from tqdm import tqdm

from utils import benchmark, get_input, test
from utils.parsing import extract_ints


def nthiter(initial):
    s = initial
    for i in range(2000):
        s ^= s * 64
        s %= 16777216
        s ^= s // 32
        s %= 16777216
        s ^= s * 2048
        s %= 16777216
    return s


def part1(raw: str):
    initials = extract_ints(raw)
    return sum(map(nthiter, initials))


def secret_stream(initial):
    s = initial
    for i in range(2000):
        s ^= s * 64
        s %= 16777216
        s ^= s // 32
        s %= 16777216
        s ^= s * 2048
        s %= 16777216
        yield s


def diff_stream(initial):
    diffs = deque()
    last = initial % 10
    for s in secret_stream(initial):
        s %= 10
        diffs.append(s - last)
        if len(diffs) == 4:
            yield tuple(diffs), s
            diffs.popleft()
        last = s


def part2(raw: str):
    initials = extract_ints(raw)
    bananas = defaultdict(dict)
    for initial in initials:
        for k, v in diff_stream(initial):
            l = bananas[k]
            if initial not in l:
                l[initial] = v
    return max(sum(v.values()) for v in tqdm(bananas.values()))


test1 = """1
10
100
2024"""

expected1 = 37327623

test2 = """1
2
3
2024"""
expected2 = 23


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
