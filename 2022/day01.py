from utils import benchmark, get_day

test = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

elves = get_day(1, test).split("\n\n")
bags = [[int(line) for line in elf.split("\n")] for elf in elves]


def part1():
    return max(sum(x) for x in bags)


def part2():
    return sum(sorted(sum(x) for x in bags)[-3:])


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
