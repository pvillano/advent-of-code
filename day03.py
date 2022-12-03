from utils import benchmark, get_day

test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

lines = get_day(3, test).split("\n")


def part1():
    tot = 0
    for line in lines:
        first_half, second_half = line[: len(line) // 2], line[len(line) // 2:]
        in_both = set(first_half) & set(second_half)
        for c in in_both:
            if "a" <= c <= "z":
                tot += ord(c) - ord("a") + 1
            else:
                tot += ord(c) - ord("A") + 27
    return tot


def part2():
    groups = zip(lines[0::3], lines[1::3], lines[2::3])
    tot = 0
    for g1, g2, g3 in groups:
        in_all = set(g1) & set(g2) & set(g3)
        for c in in_all:
            if "a" <= c <= "z":
                tot += ord(c) - ord("a") + 1
            else:
                tot += ord(c) - ord("A") + 27
    return tot


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
