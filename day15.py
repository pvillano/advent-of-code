from otqdm import otqdm
from utils import benchmark, debug_print, get_day, debug_print_sparse_grid, DEBUG

test = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
expected = 26

raw = get_day(15, test)
lines = raw.split("\n")


def part1():
    sensors = []
    sparse = dict()
    for line in lines:
        rest = line.lstrip("Sensor at x=")
        sx, rest = rest.split(", y=", 1)
        sy, rest = rest.split(": closest beacon is at x=")
        bx, by = rest.split(", y=")
        sx, sy, bx, by = map(int, (sx, sy, bx, by))
        # debug_print(sx, sy, bx, by)
        r = abs(sx - bx) + abs(sy - by)
        sensors.append((sx, sy, r))
        sparse[(sx, sy)] = "S"
        sparse[(bx, by)] = "B"
    debug_print_sparse_grid(sparse)
    # how many points cannot contain a beacon
    # how many points are closer to a sensor than that sensor's radius
    cant = set()
    if DEBUG:
        ten = 10
    else:
        ten = 2000000
    for sx, sy, sr in otqdm(sensors):
        remaining_r = sr - abs(sy - ten) + 1
        if remaining_r > 0:
            for dr in range(remaining_r):
                for a in [(sx + dr, ten), (sx - dr, ten)]:
                    assert (abs(a[0] - sx) + abs(a[1] - sy)) <= sr
                    if a not in sparse:
                        cant.add(a[0])
                        sparse[a] = "#"
    debug_print_sparse_grid(sparse)
    debug_print(min(cant), max(cant))
    return len(cant)


def covered(x, y, sensors):
    for sx, sy, sr in sensors:
        if abs(x - sx) + abs(y - sy) <= sr:
            return True
    return False


def part2():
    sensors = []
    sparse = dict()
    for line in lines:
        rest = line.lstrip("Sensor at x=")
        sx, rest = rest.split(", y=", 1)
        sy, rest = rest.split(": closest beacon is at x=")
        bx, by = rest.split(", y=")
        sx, sy, bx, by = map(int, (sx, sy, bx, by))
        # debug_print(sx, sy, bx, by)
        r = abs(sx - bx) + abs(sy - by)
        sensors.append((sx, sy, r))
        sparse[(sx, sy)] = "S"
        sparse[(bx, by)] = "B"
    debug_print_sparse_grid(sparse)
    # distress beacon in 0,4000000 not detected
    cant = set()
    sensors = sorted(sensors, key=lambda x: x[-1], reverse=True)
    debug_print(sensors)
    if DEBUG:
        y = 10
        max_incl = 20
    else:
        y = 2000000
        max_incl = 4000000
    corners = ((1, 0), (0, 1), (-1, 0), (0, -1))

    # for x in tqdm(range(max_incl+1)):
    #     for y in range(max_incl+1):
    #         if not covered(x, y, sensors):
    #             debug_print(x, y)
    #             return x * 4000000 + y
    tot = 0
    ans = None
    for y in otqdm(range(max_incl + 1)):
        windows = []
        for sx, sy, sr in sensors:
            remaining_r = sr - abs(sy - y)
            if remaining_r >= 0:
                windows.append((sx - remaining_r, sx + remaining_r))
        windows = sorted(windows)
        furthest_covered = 0
        for start, stop in windows:
            if start <= furthest_covered:
                furthest_covered = max(furthest_covered, stop)
            else:
                x = furthest_covered + 1
                ans = x * 4000000 + y
                return ans


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
