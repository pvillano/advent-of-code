from itertools import permutations, product

from utils import benchmark, get_day, test
from utils.grids import grid_index, NEWS_RC

dpad = [" ^A", "<v>"]
npad = ["789", "456", "123", " 0A"]
to_drdc = {k: v for k, v in zip("^><v", NEWS_RC)}


def npad2dirs(code):
    r, c = grid_index(npad, "A")
    output = []
    for ch in code:
        rr, cc = grid_index(npad, ch)
        dr, dc = rr - r, cc - c
        # can't just choose between
        combos = tuple(set(map(lambda x: "".join(x), permutations("v" * dr + "^" * -dr + ">" * dc + "<" * -dc))))
        trombos = []
        for comb in combos:
            rrr, ccc = r, c
            failed = False
            for d in comb:
                dr, dc = to_drdc[d]
                rrr += dr
                ccc += dc
                if rrr == 3 and ccc == 0:
                    failed = True
                    break
            if not failed:
                trombos.append(comb)
                assert rrr == rr and ccc == cc
        combos = tuple(trombos)
        assert len(combos) > 0
        output.append(combos)
        output.append(tuple("A"))
        r, c = rr, cc
    for l in product(*output):
        yield "".join(l)


# @cache
# def npad2dirs(code):
#     r, c = grid_index(npad, "A")
#     output = ""
#     for ch in code:
#         rr, cc = grid_index(npad, ch)
#         dr, dc = rr - r, cc - c
#         # prefer right before down and up before left
#         output += ">" * dc + "v" * dr + "^" * -dr + "<" * -dc + "A"
#         r, c = rr, cc
#     return output


# @cache
# def dirs2dirs(dirs):
#     r, c = grid_index(dpad, "A")
#     output = ""
#     for ch in dirs:
#         rr, cc = grid_index(dpad, ch)
#         dr, dc = rr - r, cc - c
#         # prefer down before right and left before up
#         output += "v" * dr + ">" * dc + "<" * -dc + "^" * -dr + "A"
#         r, c = rr, cc
#     return output


def dirs2dirs(codegen):
    for code in codegen:
        r, c = grid_index(dpad, "A")
        output = []
        for ch in code:
            rr, cc = grid_index(dpad, ch)
            dr, dc = rr - r, cc - c
            # can't just choose between
            combos = tuple(set(map(lambda x: "".join(x), permutations("v" * dr + "^" * -dr + ">" * dc + "<" * -dc))))
            if (r, cc) == (0, 0) or (rr, c) == (0, 0):
                trombos = []
                for comb in combos:
                    rrr, ccc = r, c
                    failed = False
                    for d in comb:
                        dr, dc = to_drdc[d]
                        rrr += dr
                        ccc += dc
                        if rrr == 0 and ccc == 0:
                            failed = True
                            break
                    if not failed:
                        trombos.append(comb)
                        assert rrr == rr and ccc == cc
                combos = tuple(trombos)
            assert len(combos) > 0
            output.append(combos)
            output.append(tuple("A"))
            r, c = rr, cc
        for l in product(*output):
            yield "".join(l)


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


def part1(raw: str):
    s = 0
    for line in raw.splitlines():
        # debug_print(npad2dirs(line))
        # debug_print(dirs2dirs(npad2dirs(line)))
        # debug_print(dirs2dirs(dirs2dirs(npad2dirs(line))))
        s += min(map(len, dirs2dirs(dirs2dirs(npad2dirs(line))))) * int(line[:-1])
    return s


def part2(raw: str):
    pass


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
        code, expected = line.split(": ")
        a1 = min(npad2dirs(code), key=len)
        assert eval_nums(a1) == code
        a2 = min(dirs2dirs(npad2dirs(code)), key=len)
        assert eval_nums(eval_dirs(a2)) == code
        a3 = min(dirs2dirs(dirs2dirs(npad2dirs(code))), key=len)
        assert eval_nums(eval_dirs(eval_dirs(a3))) == code
        assert len(a3) == len(expected)
        # 'v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA<^A>Av<A>^AA<A>Av<A<A>>^AAAvA<^A>A'
        # '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
    test(part1, test1, expected1)
    raw = get_day(21)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
