from utils import benchmark, test
from utils.advent import get_input


def parse(raw: str):
    return raw


def part1(raw: str):
    parse(raw)
    print(raw)


def part2(raw: str):
    parse(raw)


test1 = """"""

expected1 = None

test2 = test1
expected2 = None


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
