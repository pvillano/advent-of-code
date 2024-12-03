import re

from utils import benchmark, get_day, test


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret


def part1(raw: str):
    s = 0
    for match in re.finditer("mul\\((-?[0-9]+),(-?[0-9]+)\\)",raw):
        x,y = match.groups()
        x,y = map(int, [x, y])
        s += x * y
    return s


def part2(raw: str):
    s = 0
    doing = True
    # for match in re.finditer("mul\\((-?[0-9]+),(-?[0-9]+)\\)",raw):
    for match in re.finditer("(do\\(\\)|don't\\(\\))|(mul\\((-?[0-9]+),(-?[0-9]+)\\))",raw):
        dodont, mul, x, y = match.groups()
        if dodont is not None:
            doing = dodont == 'do()'
        else:
            if doing:
                x,y = map(int, [x, y])
                s += x * y

    return s


test1 = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

expected1 = 161

test2 = test1
expected2 = 48


def main():
    test(part1, test1, expected1)
    raw = get_day(3)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
