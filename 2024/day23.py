from collections import defaultdict

from utils import benchmark, get_input, test


def parse(raw: str):
    e = defaultdict(list)
    for kv in raw.splitlines():
        k,v = kv.split("-")
        e[k].append(v)
        e[v].append(k)
    return e


def part1(raw: str):
    e = parse(raw)

    seen = set()
    tris = []
    for a, bs in e.items():
        for b in bs:
            if b in seen:
                continue
            for c in e[b]:
                if c in seen or c == a:
                    continue
                if c in bs:
                    tris.append(tuple(sorted((a,b,c))))
        seen.add(a)
    tris = set(tris)
    s = 0
    for t in tris:
        for v in t:
            if v.startswith("t"):
                s += 1
                break
    return s




def part2(raw: str):
    e = parse(raw)
    def bron_kerbosch(r:set[str],p:set[str],x:set[str]):
        # r, p and x do not overlap
        if not p and not x:
            yield r
        for v in p:
            yield from bron_kerbosch(r.union([v]),p.intersection(e[v]), x.intersection(e[v]))
            p = p.difference([v])
            x = x.union([v])
    return ",".join(sorted(max(bron_kerbosch(set(), set(e.keys()), set()), key=len)))


test1 = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

expected1 = len("""co,de,ta
co,ka,ta
de,ka,ta
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn""".splitlines())

test2 = test1
expected2 = "co,de,ka,ta"


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
