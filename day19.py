from functools import cache

from tqdm import tqdm

from utils import benchmark, get_day, test


def parse(raw: str):
    first, second = raw.split("\n\n")
    towels = first.split(", ")
    patterns = second.splitlines()
    return towels, patterns

def part1(raw: str):
    towels, patterns = parse(raw)

    @cache
    def dfs(st: str):
        if not st:
            return True
        for t in towels:
            if st.startswith(t):
                if dfs(st[len(t):]):
                    return True
        return False

    s = 0
    for p in tqdm(patterns):
        if dfs(p):
            s += 1
    return s


def part2(raw: str):
    towels, patterns = parse(raw)

    @cache
    def dfs(st: str):
        if not st:
            return 1
        ways = 0
        for t in towels:
            if st.startswith(t):
                ways +=  dfs(st[len(t):])
        return ways
    s = 0
    for p in tqdm(patterns):
        s += dfs(p)
    return s


test1 = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

expected1 = 6

test2 = test1
expected2 = 16


def main():
    test(part1, test1, expected1)
    raw = get_day(19)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
