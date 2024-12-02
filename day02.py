from utils import benchmark, get_day, test, extract_ints


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(extract_ints(line))
    return ret


def part1(raw: str):
    reports = parse(raw)
    ssafe = 0
    for report in reports:
        if any([a<b for a,b in zip(report, report[1:])]) and any([a>b for a,b in zip(report, report[1:])]):
            continue # unsafe
        if all([1<=abs(a-b)<=3 for a,b in zip(report, report[1:])]):
            ssafe += 1
    return ssafe

def safe(report):
    if any([a<b for a,b in zip(report, report[1:])]) and any([a>b for a,b in zip(report, report[1:])]):
        return False
    if all([1<=abs(a-b)<=3 for a,b in zip(report, report[1:])]):
        return True
    return False

def part2(raw: str):
    reports = parse(raw)
    ssafe = 0
    for report in reports:
        if safe(report):
            ssafe += 1
            continue
        for i in range(len(report)):
            peport = [x for idx, x in enumerate(report) if idx != i]
            if safe(peport):
                ssafe += 1
                break
    return ssafe


test1 = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

expected1 = 2

test2 = test1
expected2 = 4


def main():
    test(part1, test1, expected1)
    raw = get_day(2)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
