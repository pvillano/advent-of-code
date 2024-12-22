from functools import cache
from itertools import permutations, product

from utils import benchmark, get_day, test
from utils.grids import grid_index, NEWS_RC

dpad = [" ^A", "<v>"]
npad = ["789", "456", "123", " 0A"]
to_drdc = {k: v for k, v in zip("^><v", NEWS_RC)}


def crosses30(start_r, start_c, ends_in_a):
    assert ends_in_a[-1] == "A"
    r, c = start_r, start_c
    for ch in ends_in_a[:-1]:
        dr, dc = to_drdc[ch]
        r += dr
        c += dc
        if r == 3 and c == 0:
            return True
    return False


def code_expansions(code) -> tuple[tuple[str, ...], ...]:
    r, c = grid_index(npad, "A")
    garden_path: list[list[str, ...], ...] = []
    for ch in code:
        next_r, next_c = grid_index(npad, ch)
        dr, dc = next_r - r, next_c - c
        candidates = tuple(
            set(map(lambda x: "".join(x) + "A", permutations("v" * dr + "^" * -dr + ">" * dc + "<" * -dc)))
        )
        valid_candidates = [cand for cand in candidates if not crosses30(r, c, cand)]
        assert len(valid_candidates) > 0
        garden_path.append(valid_candidates)
        r, c = next_r, next_c
    return tuple(product(*garden_path))


def crosses0(start_r, start_c, ends_in_a):
    assert ends_in_a[-1] == "A"
    r, c = start_r, start_c
    for ch in ends_in_a[:-1]:
        dr, dc = to_drdc[ch]
        r += dr
        c += dc
        if r == c == 0:
            return True
    return False


@cache
def possible_expansions(ends_in_a: str) -> tuple[tuple[str, ...], ...]:
    r, c = grid_index(dpad, "A")
    garden_path: list[list[str, ...], ...] = []
    for ch in ends_in_a:
        next_r, next_c = grid_index(dpad, ch)
        dr, dc = next_r - r, next_c - c
        candidates = tuple(
            set(map(lambda x: "".join(x) + "A", permutations("v" * dr + "^" * -dr + ">" * dc + "<" * -dc)))
        )
        valid_candidates = [cand for cand in candidates if not crosses0(r, c, cand)]
        assert len(valid_candidates) > 0
        garden_path.append(valid_candidates)
        r, c = next_r, next_c
    return tuple(product(*garden_path))


def eval_dirs(dirs):
    r, c = grid_index(dpad, "A")
    out = ""
    for d in dirs:
        if d == "A":
            out += dpad[r][c]
            continue
        dr, dc = to_drdc[d]
        r += dr
        c += dc
    return out


def eval_nums(dirs):
    r, c = grid_index(npad, "A")
    out = ""
    for d in dirs:
        if d == "A":
            out += npad[r][c]
            continue
        dr, dc = to_drdc[d]
        r += dr
        c += dc
    return out


@cache
def cost_of_expansion(end_in_a: str, times_expanding: int) -> int:
    assert end_in_a[-1] == "A"
    assert times_expanding > 0
    all_expansions = possible_expansions(end_in_a)
    if times_expanding == 1:
        combined_lengths = [sum(len(token) for token in expansion) for expansion in all_expansions]
        return min(combined_lengths)
    combined_lengths = [
        sum(cost_of_expansion(token, times_expanding - 1) for token in expansion) for expansion in all_expansions
    ]
    return min(combined_lengths)


def part1(raw: str, two=2):
    s = 0
    for code in raw.splitlines():
        numeric_part = int(code[:-1])
        len_shortest_sequence = min(
            sum(cost_of_expansion(token, two) for token in code_expansion) for code_expansion in code_expansions(code)
        )
        s += len_shortest_sequence * numeric_part
    return s


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

test2 = test1
expected2 = None


def main():
    for line in test0.splitlines():
        code, answer = line.split(": ")
        expected = int(code[:-1]) * len(answer)
        test(part1, code, expected)
    test(part1, test1, expected1)
    raw = get_day(21)
    assert benchmark(part1, raw) == 248684
    assert benchmark(part2, raw) == 307055584161760


if __name__ == "__main__":
    main()
