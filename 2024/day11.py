from collections import Counter

from utils import benchmark, get_input, test
from utils.parsing import extract_ints


def blink(stones):
    for s in stones:
        strs = str(s)
        if s == 0:
            yield 1
        elif len(strs) % 2 == 0:
            yield int(strs[: len(strs) // 2])
            yield int(strs[len(strs) // 2 :])
        else:
            yield s * 2024


def parse(raw: str):
    return list(extract_ints(raw))


def ilen(it):
    s = 0
    for _ in it:
        s += 1
    return s


def part1(raw: str):
    return ilen(
        blink(
            blink(
                blink(
                    blink(
                        blink(
                            blink(
                                blink(
                                    blink(
                                        blink(
                                            blink(
                                                blink(
                                                    blink(
                                                        blink(
                                                            blink(
                                                                blink(
                                                                    blink(
                                                                        blink(
                                                                            blink(
                                                                                blink(
                                                                                    blink(
                                                                                        blink(
                                                                                            blink(
                                                                                                blink(
                                                                                                    blink(
                                                                                                        blink(
                                                                                                            map(
                                                                                                                int,
                                                                                                                raw.split(),
                                                                                                            )
                                                                                                        )
                                                                                                    )
                                                                                                )
                                                                                            )
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )


def part2(raw: str):
    stones = Counter(parse(raw))
    for _ in range(75):
        new_stones = Counter()
        for k, v in stones.items():
            if k == 0:
                new_stones[1] += v
            else:
                strk = str(k)
                if len(strk) % 2 == 0:
                    new_stones[int(strk[: len(strk) // 2])] += v
                    new_stones[int(strk[len(strk) // 2 :])] += v
                else:
                    new_stones[k * 2024] += v
        stones = new_stones
    return sum(stones.values())


test1 = """125 17"""

expected1 = 55312

test2 = test1

expected2 = 65601038650482


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
