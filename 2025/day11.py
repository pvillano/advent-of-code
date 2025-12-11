from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
from functools import cache

from utils import benchmark, test
from utils.advent import get_input
from utils.graphs import reverse_edges, is_dag, topological_sort
from utils.itertools2 import degenerate


# @degenerate
def parse(raw: str):
    d = dict()
    for line in raw.splitlines():
        key, *values = line.split(" ")
        key = key[:-1]
        d[key] = values
    d["out"] = []
    return d


# def part1(raw: str):
#     all_nodes = parse(raw)
#     s = 0
#     def dfs(node):
#         if node == "out":
#             yield 1
#             return
#         for child in all_nodes[node]:
#             yield from dfs(child)
#     return sum(dfs("you"))

def part1(raw: str):
    to_child = parse(raw)

    to_parent: dict[str, list[str]] = reverse_edges(to_child)
    ways_to_here = defaultdict(int)
    ways_to_here['you'] = 1

    orphans = ['lmao']
    while orphans:
        orphans = [k for k, v in to_parent.items() if len(v) == 0]
        # parents pass gifts to their children
        for parent in orphans:
            for child in to_child[parent]:
                ways_to_here[child] += ways_to_here[parent]
        # and then the children forget those parents
        for parent in orphans:
            for child in to_child[parent]:
                to_parent[child].remove(parent)
                # may become next generation of orphan
        # and then the parents themselves are forgotten
        for parent in orphans:
            del to_parent[parent]
    return ways_to_here["out"]


# pathvector = namedtuple("pathvector", "total dac fft both", defaults=(0,0,0,0))
@dataclass
class pathvector:
    total: int = 0
    fft: int = 0
    dac: int = 0
    both: int = 0



def vectoradd(outvec: pathvector, invec: pathvector, parent_id):
    assert invec.total >= invec.dac >= invec.both
    assert invec.total >= invec.fft >= invec.both

    outvec.total += invec.total
    if parent_id == 'fft':
        outvec.dac += invec.dac
        outvec.fft += invec.total
        outvec.both += invec.dac
    elif parent_id == 'dac':
        outvec.dac += invec.total
        outvec.fft += invec.fft
        outvec.both += invec.fft
    else:
        outvec.dac += invec.dac
        outvec.fft += invec.fft
        outvec.both += invec.both


def part2(raw: str):
    to_child = parse(raw)

    to_parent: dict[str, list[str]] = reverse_edges(to_child)
    ways_to_here = defaultdict(pathvector)
    ways_to_here['svr'] = pathvector(1,0,0,0)

    orphans = ['lmao']
    while orphans:
        orphans = [k for k, v in to_parent.items() if len(v) == 0]
        # parents pass gifts to their children
        for parent in orphans:
            for child in to_child[parent]:
                vectoradd(ways_to_here[child], ways_to_here[parent], parent)
        # and then the children forget those parents
        for parent in orphans:
            for child in to_child[parent]:
                to_parent[child].remove(parent)
                # may become next generation of orphan
        # and then the parents themselves are forgotten
        for parent in orphans:
            del to_parent[parent]
    return ways_to_here["out"].both


def part2vis(raw: str):
    import graphviz
    dot = graphviz.Digraph()
    all_nodes = parse(raw)
    for k, v in all_nodes.items():
        dot.node(k)
        for vv in v:
            dot.edge(vv, k)
    dot.render("day11", view=True)


test1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

expected1 = 5

test2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
expected2 = 2


def main():
    raw = get_input(__file__)

    # for k,v in parse(raw).items():
    #     print(k)
    # for k, v in parse(test2).items():
    #     for vv in v:
    #         print(f'{{source: "{k}", target: "{vv}", type: "suit"}},')
    # part2vis(raw)
    # exit(0)

    # test(part1, test1, expected1)
    # benchmark(part1, raw)

    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
