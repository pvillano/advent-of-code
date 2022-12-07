import json
from collections import defaultdict, deque, Counter
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, reduce
from itertools import (
    accumulate,
    count,
    cycle,
    product,
    permutations,
    combinations,
    pairwise,
)
from math import sqrt, floor, ceil, gcd, sin, cos, atan2

from otqdm import otqdm

from utils import benchmark, debug_print, get_day, pipe

test = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

lines = get_day(7, test).split("\n")


def jsonify(lines: list[str]):
    stack = []
    cur_dir = []
    yield "["
    for line in lines[1:]:
        tokens = line.split()
        if line == "$ ls":
            yield "["
        elif line == "$ cd ..":
            yield "],"
        elif line.startswith("$ cd"):
            pass
        elif tokens[0] == "dir":
            pass
        elif tokens[0].isnumeric():
            yield tokens[0] + ","
        else:
            raise ValueError("unknown " + line)
    yield "]"

# returns suminside, sumsmallinside
def recurse(l):
    if type(l) == int:
        return l, 0
    elif type(l) == list:
        suminside = 0
        sumsmallinside = 0
        for i in l:
            si, ss = recurse(i)
            suminside += si
            sumsmallinside += ss
        if suminside < 100000:
            sumsmallinside += suminside
        return suminside, sumsmallinside




def part1():
    line_ptr = 0
    myson = "".join(jsonify(lines)).replace(",]", "]")
    rcount = myson.count("[") - myson.count("]")
    myson += "".join(["]"] * rcount)
    myson = json.loads(myson)
    debug_print(myson)
    return recurse(myson)[1]


# returns suminside
def recurse2(l, g):
    if type(l) == int:
        return l
    elif type(l) == list:
        suminside = 0
        for i in l:
            si = recurse2(i,g)
            suminside += si
        g.append(suminside)
        return suminside

def part2():
    myson = "".join(jsonify(lines)).replace(",]", "]")
    rcount = myson.count("[") - myson.count("]")
    myson += "".join(["]"] * rcount)
    myson = json.loads(myson)
    debug_print(myson)
    g = []
    sum_all = recurse2(myson, g)
    debug_print(sum_all)
    used = sum_all
    unused = 70000000 - used
    additional_needed = 30000000 - unused
    debug_print(f"{used=} {unused=} {additional_needed=}")
    return min(filter(lambda x: x >= additional_needed, g))



if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
