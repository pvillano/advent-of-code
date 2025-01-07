import operator

from utils import benchmark, get_day, flatten

test = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

raw = get_day(21, test)
lines = raw.split("\n")


def parse():
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }
    leaves, nodes = dict(), dict()
    for line in lines:
        key, val = line.split(": ")
        if " " in val:
            val = val.split(" ")
            assert len(val) == 3
            val[1] = ops[val[1]]
            nodes[key] = val
        else:
            val = int(val)
            leaves[key] = val
    return nodes, leaves


def part1():
    nodes, leaves = parse()
    all_children = set(flatten(nodes.values()))
    root = set(nodes) - all_children
    assert len(root) == 1
    root = list(root)[0]

    def rec(node_name):
        if node_name in leaves:
            return leaves[node_name]
        c1, op, c2 = nodes[node_name]
        return op(rec(c1), rec(c2))

    return rec(root)


def parse2():
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }
    nodes = dict()
    for line in lines:
        key, val = line.split(": ")
        if " " in val:
            val = val.split(" ")
            assert len(val) == 3
            val[1] = ops[val[1]]
            nodes[key] = val
        else:
            val = int(val)
            nodes[key] = val
    return nodes


def part2():
    unop = {
        operator.add: operator.sub,
        operator.sub: operator.add,
        operator.mul: operator.truediv,
        operator.truediv: operator.mul
    }

    nodes = parse2()
    all_children = set(flatten(x for x in nodes.values() if not isinstance(x, int)))
    root = set(nodes.keys()) - all_children
    assert len(root) == 1
    root = list(root)[0]

    def rec(node_name):
        if node_name == "humn":
            return "humn"
        if not isinstance(nodes[node_name], list):
            return nodes[node_name]
        left_name, op, right_name = nodes[node_name]
        left_val, right_val = rec(left_name), rec(right_name)
        if left_val == "humn" or right_val == "humn":
            return "humn"
        return op(left_val, right_val)

    while "humn" not in nodes[root]:
        left_name, _, right_name = nodes[root]
        left_val, right_val = rec(left_name), rec(right_name)
        if left_val == "humn":
            assert right_val != "humn"
            new_parent = left_name
            other_side = right_val
        else:
            assert right_val == "humn"
            new_parent = right_name
            other_side = left_val
        inner_left_name, op, inner_right_name = nodes[new_parent]
        inner_left_val, inner_right_val = rec(inner_left_name), rec(inner_right_name)

        if inner_left_val == "humn":
            # we know humn op inner_right_val == right_val
            nodes[inner_right_name] = unop[op](other_side, inner_right_val)
        else:
            assert inner_right_val == "humn"
            # we know inner_left_val op humn == right_val
            if op == operator.sub:  # x - humn = y ==> humn = x - y
                nodes[inner_left_name] = inner_left_val - other_side
            elif op == operator.add:  # x + humn = y ==> humn = y - x
                nodes[inner_left_name] = other_side - inner_left_val
            elif op == operator.truediv:  # x - humn = y ==> humn = x - y
                nodes[inner_left_name] = inner_left_val / other_side
            elif op == operator.mul:  # x + humn = y ==> humn = y - x
                nodes[inner_left_name] = other_side / inner_left_val
        root = new_parent
    return rec(nodes[root][0]), rec(nodes[root][2]),


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
