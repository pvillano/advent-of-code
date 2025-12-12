from utils import benchmark
from utils.advent import get_input
from utils.parsing import extract_ints

def part1(raw: str):
    *present_str_list, regions_str = raw.split("\n\n")
    presents = [p.count('#') for p in present_str_list]
    regions = [extract_ints(line) for line in regions_str.splitlines()]
    s = 0
    for length, width, *counts in regions:
        area = length * width
        used_area = sum(cnt * presents[i] for i, cnt in enumerate(counts))
        if used_area / area <= 1:
            s += 1
    return s


def main():
    raw = get_input(__file__)
    benchmark(part1, raw)


if __name__ == "__main__":
    main()
