from itertools import groupby, batched

from tqdm import tqdm

from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate
from utils.printing import debug_print


@degenerate
def parse(raw: str):
    for line in raw.split(','):
        a, b = line.split('-')
        yield int(a), int(b)


def part1(raw: str):
    sumall = 0
    for a,b in tqdm(parse(raw)):
        for i in range(a,b+1):
            s = str(i)
            if len(s) % 2 == 0 and s[len(s)//2:] == s[:len(s)//2]:
                sumall += i
    return sumall


def part2(raw: str):
    sumall = 0
    for a,b in (parse(raw)):
        for i in range(a,b+1):
            s = str(i)
            for group_size in range(1, len(s)//2+1):
                groups = set(batched(s, group_size))
                if len(groups) == 1:
                    debug_print(i)
                    sumall += i
                    break
    return sumall


test1 = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

expected1 = 1227775554

test2 = test1
expected2 = 4174379265


def main():
    raw = get_input(__file__)
    test(part1, test1, expected1)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
