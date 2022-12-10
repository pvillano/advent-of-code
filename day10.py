from utils import benchmark, get_day

test = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
raw = get_day(10, test)
lines = raw.split("\n")

strengths = range(20, 221, 40)


def expand():
    for line in lines:
        if line == "noop":
            yield 0
        else:
            yield 0
            op, val = line.split()
            yield int(val)


def part1():
    tot = 0
    x = 1
    for idx, val in enumerate(expand()):
        idx += 2
        x += val
        # debug_print(f"{idx=} {x=}")
        if idx in strengths:
            # debug_print(f"{idx=} {x*idx=}")
            tot += x * idx
    return x, tot


def part2():
    display = [['.'] * 40 for _ in range(6)]
    x = 1
    for idx, val in enumerate(expand()):
        idx += 1
        x += val
        if (idx % 40) in (x - 1, x, x + 1):
            row, col = divmod(idx % 240, 40)
            display[row][col] = "#"
    print(*["".join(x) for x in display], sep="\n")


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
