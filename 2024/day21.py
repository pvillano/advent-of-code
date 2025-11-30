from functools import cache
from itertools import permutations, product

from utils import benchmark, get_input, test
from utils.grids import grid_index, NEWS_RC

dpad = [" ^A", "<v>"]
npad = ["789", "456", "123", " 0A"]
to_drdc = {k: v for k, v in zip("^><v", NEWS_RC)}


def crosses(bad_r, bad_c, start_r, start_c, ends_in_a):
    r, c = start_r, start_c
    for ch in ends_in_a[:-1]:
        dr, dc = to_drdc[ch]
        r += dr
        c += dc
        if r == bad_r and c == bad_c:
            return True
    return False


@cache
def all_expansions(ends_in_a: str) -> tuple[tuple[str, ...], ...]:
    if ends_in_a[:-1].isnumeric():
        pad = npad
        bad_r, bad_c = 3, 0
    else:
        pad = dpad
        bad_r, bad_c = 0, 0
    r, c = grid_index(pad, "A")
    path: list[list[str, ...], ...] = []
    for ch in ends_in_a:
        next_r, next_c = grid_index(pad, ch)
        dr, dc = next_r - r, next_c - c
        candidates = set(map(lambda x: "".join(x) + "A", permutations("v" * dr + "^" * -dr + ">" * dc + "<" * -dc)))
        path.append([cand for cand in candidates if not crosses(bad_r, bad_c, r, c, cand)])
        r, c = next_r, next_c
    return tuple(product(*path))


@cache
def cost(end_in_a: str, robot_cnt: int) -> int:
    if robot_cnt == 0:
        return len(end_in_a)
    return min(sum(cost(token, robot_cnt - 1) for token in expansion) for expansion in all_expansions(end_in_a))


def part1(raw: str, num_robots=2):
    return sum(
        min(sum(cost(token, num_robots) for token in token_list) for token_list in all_expansions(code))
        * int(code[:-1])
        for code in raw.splitlines()
    )


def part2(raw: str):
    return part1(raw, 25)


test1 = """029A
980A
179A
456A
379A"""

test0 = """029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"""

expected1 = 126384


def main():
    for line in test0.splitlines():
        code, answer = line.split(": ")
        expected = int(code[:-1]) * len(answer)
        test(part1, code, expected)
    test(part1, test1, expected1)
    raw = get_input(__file__)
    assert benchmark(part1, raw) == 248684
    assert benchmark(part2, raw) == 307055584161760


if __name__ == "__main__":
    main()
