import graphviz
from z3 import Bool, Solver, BoolRef, prove, unsat

from utils import benchmark, get_day
from utils.printing import debug_print


def parse(raw: str):
    return


def part1(raw: str):
    s = Solver()
    d = dict()
    initial_str, relations_str = raw.split("\n\n")
    for i in initial_str.splitlines():
        k, v_str = i.split(": ")
        v = int(v_str)
        var = Bool(k)
        d[k] = var
        s.add(var == bool(v))
    for r in relations_str.splitlines():
        a, op_str, b, _, c = r.split(" ")
        for v in [a, b, c]:
            if v not in d:
                d[v] = Bool(v)
        match op_str:
            case "AND":
                s.add(d[a] & d[b] == d[c])
            case "OR":
                s.add(d[a] | d[b] == d[c])
            case "XOR":
                s.add(d[a] ^ d[b] == d[c])
            case _:
                assert False
    s.check()
    ans = 0
    for z_key, z_val in sorted((zk for zk in d.items() if zk[0].startswith("z")), reverse=True):
        ans <<= 1
        x: BoolRef = s.model().eval(z_val)
        debug_print(z_key, x)
        ans += int(bool(x))
    return ans


def part2fail(raw: str):
    """
    # 45bit + 45bit -> 46bit
    # contains 89 xor, ie minimal
    # contains 89 and ie minimal
    # contains 44 or, ie minimal
    half-sum, full-sum
    carry-carry
    half carry, full carry

    a xor is correct if it
        matches x** ^ y** -> xor_input


    """
    initial_str, relations_str = raw.split("\n\n")
    n = len(initial_str.splitlines()) // 2

    q1 = []
    q2 = []
    half_sum: list[str | None] = [None] * n
    for r in relations_str.splitlines():
        a, op_str, b, _, c = r.split(" ")
        a, b = sorted([a, b])
        q1.append((a, op_str, b, c))

    for a, op_str, b, c in q1:
        if a[0] == "x" and b[0] == "y" and op_str == "XOR" and a[1:] == b[1:]:
            k = int(a[1:])
            half_sum[k] = c
            assert not c.startswith("z") or c == "z00"
        else:
            q2.append((a, op_str, b, c))
    assert len(q1) - len(q2) == n

    q3 = []
    half_carry: list[str | None] = [None] * n
    for a, op_str, b, c in q2:
        if a[0] == "x" and b[0] == "y" and op_str == "AND" and a[1:] == b[1:]:
            k = int(a[1:])
            half_carry[k] = c
            assert not c.startswith("z")
        else:
            q3.append((a, op_str, b, c))
    assert len(q2) - len(q3) == n

    # half_sum and half carry can have wrong outputs but not wrong inputs

    d = {(a, op_str, b): c for (a, op_str, b, c) in q3}

    pass


def find1(l, lamb):
    r = []
    for i in l:
        if lamb(*i):
            r.append(i)
            if len(r) > 1:
                raise IndexError("too many matches")
    if len(r) == 0:
        raise IndexError("no matches")
    return r[0]


def arg_find1(l, lamb) -> int:
    r = []
    for i, x in enumerate(l):
        if lamb(x):
            r.append(i)
            if len(r) > 1:
                raise IndexError("too many matches")
    if len(r) == 0:
        raise IndexError("no matches")
    return r[0]


def parse2(raw):
    initial_str, relations_str = raw.split("\n\n")

    n = len(initial_str.splitlines()) // 2

    q1 = []
    for r in relations_str.splitlines():
        a, op_str, b, _, c = r.split(" ")
        a, b = sorted([a, b])
        q1.append([a, op_str, b, c])
    return q1, n


def part2fail2(raw):
    q1, n = parse2(raw)

    swapped_outputs = []

    def swap_outputs(wire1, wire2):
        arg1 = arg_find1(q1, lambda _, __, ___, wire: wire == wire1)
        arg2 = arg_find1(q1, lambda _, __, ___, wire: wire == wire2)
        q1[arg1][-1], q1[arg2][-1] = q1[arg2][-1], q1[arg1][-1]
        swapped_outputs.append(wire1)
        swapped_outputs.append(wire2)

    # z all outs?
    for i in range(n):
        a, op_str, b, c = q1[i]
        if a[0] != "x" or b[0] != "y" and op_str == "XOR":
            assert a[0] != "x" and b[0] != "y"
            assert c[0] == "z"

    for i in range(n):
        if i == 0:
            half_sum = find1(q1, lambda a, op_str, b, c: a == "x00" and b == "y00" and op_str == "XOR")
            if half_sum[-1] != "z00":
                raise NotImplementedError()
            prev_carry = find1(q1, lambda a, op_str, b, c: a == "x00" and b == "y00" and op_str == "XOR")
            continue
        half_sum = find1(q1, lambda a, op_str, b, c: a == f"x{i:02}" and b == f"y{i:02}" and op_str == "XOR")
        half_carry = find1(q1, lambda a, op_str, b, c: a == f"x{i:02}" and b == f"y{i:02}" and op_str == "AND")
        full_sum = find1(q1, lambda a, op_str, b, c: c == f"z{i:02}")
        assert full_sum[1] == "AND"


def part2fail3(raw):
    q1, n = parse2(raw)
    dot = graphviz.Digraph()
    for i in range(n):
        dot.node(f"x{i:02}")
        dot.node(f"y{i:02}")
        dot.node(f"z{i:02}")
    dot.node(f"z{n:02}")
    for a, op_str, b, c in q1:
        dot.node(c, f"{a} {op_str} {b} = {c}")
        dot.edge(a, c)
        dot.edge(b, c)
    dot.render("21.gv")


def part2fail4(raw):
    s = Solver()
    d = dict()
    initial_str, relations_str = raw.split("\n\n")
    n = len(initial_str.splitlines()) // 2
    for i in initial_str.splitlines():
        k, _ = i.split(": ")
        var = Bool(k)
        d[k] = var

    for r in relations_str.splitlines():
        a, op_str, b, _, c = r.split(" ")
        for v in [a, b, c]:
            if v not in d:
                d[v] = Bool(v)
        match op_str:
            case "AND":
                s.add(d[a] & d[b] == d[c])
            case "OR":
                s.add(d[a] | d[b] == d[c])
            case "XOR":
                s.add(d[a] ^ d[b] == d[c])
            case _:
                assert False

    for i in range(n):
        for j in ["hs", "fs", "cc", "hc", "fc"]:
            d[f"{j}{i:02}"] = Bool(f"{j}{i:02}")
        if i == 0:
            cin = False
        else:
            cin = d[f"fc{i-1:02}"]
        s.add(d[f"hs{i:02}"] == d[f"x{i:02}"] ^ d[f"y{i:02}"])
        s.add(d[f"fs{i:02}"] == d[f"hs{i:02}"] ^ cin)
        s.add(d[f"cc{i:02}"] == d[f"hs{i:02}"] & cin)
        s.add(d[f"hc{i:02}"] == d[f"x{i:02}"] & d[f"y{i:02}"])
        s.add(d[f"fc{i:02}"] == d[f"cc{i:02}"] & d[f"hc{i:02}"])

        print(i, s.check(d[f"fs{i:02}"] != d[f"z{i:02}"]))

        s.add(d[f"fs{i:02}"] == d[f"z{i:02}"])


def norm(a, op, b):
    a, b = sorted([a, b])
    return a, op, b


def swap(raw: str, a: str, b: str):
    assert "@" not in raw
    raw = raw.replace(a, "@")
    raw = raw.replace(b, a)
    raw = raw.replace("@", b)
    return raw


def part2(raw):
    raw = swap(raw, "-> thm", "-> z08")
    raw = swap(raw, "-> wrm", "-> wss")
    raw = swap(raw, "-> hwq", "-> z22")
    raw = swap(raw, "-> gbs", "-> z29")

    return ",".join(sorted(("thm", "z08", "wrm", "wss", "hwq", "z22", "gbs", "z29")))

    initial_str, relations_str = raw.split("\n\n")
    n = len(initial_str.splitlines()) // 2
    raw_graph = dict()
    for r in relations_str.splitlines():
        a, op_str, b, _, c = r.split(" ")
        raw_graph[norm(a, op_str, b)] = c

    assert ("x00", "XOR", "y00") in raw_graph
    fs = raw_graph[("x00", "XOR", "y00")]
    assert fs == "z00"
    assert ("x00", "AND", "y00") in raw_graph
    fc = raw_graph[("x00", "AND", "y00")]
    for i in range(1, n):
        cin = fc
        x, y, z = f"x{i:02}", f"y{i:02}", f"z{i:02}"
        assert norm(x, "XOR", y) in raw_graph
        hs = raw_graph[norm(x, "XOR", y)]
        assert norm(hs, "XOR", cin) in raw_graph
        fs = raw_graph[norm(hs, "XOR", cin)]
        assert fs == z
        assert norm(x, "AND", y) in raw_graph
        hc = raw_graph[norm(x, "AND", y)]
        assert norm(hs, "AND", cin) in raw_graph
        cc = raw_graph[norm(hs, "AND", cin)]
        assert norm(hc, "OR", cc) in raw_graph
        fc = raw_graph[norm(hc, "OR", cc)]


test1 = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

expected1 = 4

test2 = test1
expected2 = None


def main():
    # test(part1, test1, expected1)
    raw = get_day(24)
    # benchmark(part1, raw)
    # test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
