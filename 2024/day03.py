import re
from operator import mul

from utils import benchmark, get_day, test


def part1(raw: str):
    return sum(mul(*map(int, match.groups())) for match in re.finditer("mul\\((-?[0-9]+),(-?[0-9]+)\\)", raw))


def part2(raw: str):
    s = 0
    doing = True
    for match in re.finditer("(do\\(\\)|don't\\(\\))|(mul\\((-?[0-9]+),(-?[0-9]+)\\))", raw):
        do_or_dont, _, x, y = match.groups()
        if do_or_dont is not None:
            doing = do_or_dont == "do()"
        else:
            if doing:
                x, y = map(int, [x, y])
                s += x * y
    return s


def part2second_solution(raw: str):
    s = 0
    doing = True
    do_matches = list(re.finditer("(do|don't)\\(\\)", raw))
    mul_matches = list(re.finditer("mul\\((-?[0-9]+),(-?[0-9]+)\\)", raw))
    matches = sorted(do_matches + mul_matches, key=lambda x: x.start())
    for match in matches:
        if match.groups()[0] == "do":
            doing = True
        elif match.groups()[0] == "don't":
            doing = False
        elif doing:
            x, y = map(int, match.groups())
            s += x * y
    return s


test1 = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

expected1 = 161

test2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
expected2 = 48


def main():
    test(part1, test1, expected1)
    raw = get_day(3)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)
    test(part2second_solution, test2, expected2)
    benchmark(part2second_solution, raw)


if __name__ == "__main__":
    main()
