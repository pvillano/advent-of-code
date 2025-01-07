from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate


@degenerate
def parse(raw: str):
    for line in raw.splitlines():
        line = line.removeprefix("+")
        yield int(line)



def part1(raw: str):
    return sum(parse(raw))


def part2(raw: str):
    parse(raw)


test1 = """+1
+1
-2"""

expected1 = 0

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
