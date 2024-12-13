from utils import test, get_day, benchmark
from utils.parsing import extract_ints
from utils.printing import debug_print

ACOST = 3
BCOST = 1


def parse(raw: str):
    games = raw.split("\n\n")
    l = []
    for g in games:
        ax, ay, bx, by, px, py = extract_ints(g)
        l.append((ax, ay, bx, by, px, py))
    return l


def part1(raw: str):
    games = parse(raw)
    s = 0
    for idx, (ax, ay, bx, by, px, py) in enumerate(games):
        a, b, c, d = ax, bx, ay, by

        invdet = a * d - b * c
        sola, solb = d * px + -b * py, -c * px + a * py
        sola /= invdet
        solb /= invdet
        debug_print(f"{sola=} {solb=}")
        if sola % 1 == 0 and solb % 1 == 0:
            s += sola * ACOST + solb * BCOST
    return s


def parse2(raw: str):
    games = raw.split("\n\n")
    l = []
    for g in games:
        ax, ay, bx, by, px, py = extract_ints(g)
        px += 10000000000000
        py += 10000000000000
        l.append((ax, ay, bx, by, px, py))
    return l

def part2(raw: str):
    games = parse2(raw)
    s = 0
    for idx, (ax, ay, bx, by, px, py) in enumerate(games):
        a, b, c, d = ax, bx, ay, by

        invdet = a * d - b * c
        sola, solb = d * px + -b * py, -c * px + a * py
        sola /= invdet
        solb /= invdet
        debug_print(f"{sola=} {solb=}")
        if sola % 1 == 0 and solb % 1 == 0:
            s += sola * ACOST + solb * BCOST
    return s


test1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

expected1 = 480

test2 = test1
expected2 = 875318608908


def main():
    test(part1, test1, expected1)
    raw = get_day(13)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
