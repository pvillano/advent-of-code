from utils import benchmark, get_day

test = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

raw = get_day(9, test)
lines = raw.split("\n")

dirmap = {
    "R": (1, 0),
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1),
}


def single_stepper():
    for line in lines:
        direction, dist = line.split()
        direction = dirmap[direction]
        dist = int(dist)
        for i in range(dist):
            yield direction


def part1():
    hx, hy, tx, ty = 0, 0, 0, 0
    seen = {(0, 0)}
    for dx, dy in single_stepper():
        hx += dx
        hy += dy
        if abs(hx - tx) == 2:
            if abs(hy - ty) == 1:
                ty = hy
            tx = (hx + tx) / 2
            seen.add((tx, ty))
        elif abs(hy - ty) == 2:
            if abs(hx - tx) == 1:
                tx = hx
            ty = (hy + ty) / 2
            seen.add((tx, ty))
    return len(seen)


def propagate(knots):
    for idx in range(1, len(knots)):
        hx, hy = knots[idx - 1]
        tx, ty = knots[idx]
        if abs(hx - tx) == 2:
            if abs(hy - ty) == 2:
                ty = (hy + ty) / 2
            elif abs(hy - ty) == 1:
                ty = hy
            tx = (hx + tx) / 2
        elif abs(hy - ty) == 2:
            assert abs(hx - tx) < 2
            if abs(hx - tx) == 1:
                tx = hx
            ty = (hy + ty) / 2
        else:
            assert abs(hx - tx) < 2
            assert abs(hy - ty) < 2
        knots[idx] = (tx, ty)


def part2():
    knots = [[0, 0] for _ in range(10)]
    seen = {(0, 0)}
    for dx, dy in single_stepper():
        knots[0][0] += dx
        knots[0][1] += dy
        propagate(knots)
        seen.add(knots[-1])
    return len(seen)


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
