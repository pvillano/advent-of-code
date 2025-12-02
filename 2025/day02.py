from itertools import batched

from utils import benchmark, test
from utils.advent import get_input
from utils.itertools2 import degenerate
from utils.printing import debug_print


@degenerate
def parse(raw: str):
    for line in raw.split(','):
        lower, upper_inclusive = line.split('-')
        yield int(lower), int(upper_inclusive)


def part1(raw: str):
    gift_ids_sum = 0
    for lower, upper_inclusive in parse(raw):
        for gift_id in range(lower, upper_inclusive + 1):
            id_str = str(gift_id)
            if id_str[len(id_str) // 2:] == id_str[:len(id_str) // 2]:
                gift_ids_sum += gift_id
    return gift_ids_sum


def part2(raw: str):
    gift_ids_sum = 0
    for lower, upper_inclusive in parse(raw):
        for gift_id in range(lower, upper_inclusive + 1):
            id_str = str(gift_id)
            for chunk_size in range(1, len(id_str) // 2 + 1):
                unique_chunks = set(batched(id_str, chunk_size))
                if len(unique_chunks) == 1:
                    debug_print(gift_id)
                    gift_ids_sum += gift_id
                    break
    return gift_ids_sum


test1 = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

expected1 = 1227775554

test2 = test1
expected2 = 4174379265


def main():
    raw = get_input(__file__)
    test(part1, test1, expected1)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
