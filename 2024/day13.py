from utils import test, get_input, benchmark
from utils.parsing import extract_ints


def part1(raw: str, d=0):
    games = raw.split("\n\n")
    s = 0
    for g in games:
        ax, ay, bx, by, px, py = extract_ints(g)
        px, py = px + d, py + d
        inv_det = ax * by - bx * ay
        a, b = by * px + -bx * py, -ay * px + ax * py
        if a % inv_det == 0 and b % inv_det == 0:
            s += 3 * a // inv_det + b // inv_det
    return s


def part2(raw: str):
    return part1(raw, 10000000000000)


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
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
