import json
import re
from typing import SupportsIndex

from utils import benchmark, debug_print, get_day

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


def jsonify():
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


# returns sum_inside, sum_small_inside
def recurse(l):
    if isinstance(l, int):
        return l, 0
    elif isinstance(l, list):
        sum_inside = 0
        sum_small_inside = 0
        for i in l:
            si, ss = recurse(i)
            sum_inside += si
            sum_small_inside += ss
        if sum_inside < 100000:
            sum_small_inside += sum_inside
        return sum_inside, sum_small_inside


def part1():
    myson = "".join(jsonify()).replace(",]", "]")
    rcount = myson.count("[") - myson.count("]")
    myson += "".join(["]"] * rcount)
    myson = json.loads(myson)
    debug_print(myson)
    return recurse(myson)[1]


# returns sum_inside
def recurse2(l, g):
    if isinstance(l, int):
        return l
    elif isinstance(l, list):
        sum_inside = 0
        for i in l:
            si = recurse2(i, g)
            sum_inside += si
        g.append(sum_inside)
        return sum_inside


def part2():
    myson = "".join(jsonify()).replace(",]", "]")
    rcount = myson.count("[") - myson.count("]")
    myson += "".join(["]"] * rcount)
    myson = json.loads(myson)
    g = []
    used = recurse2(myson, g)
    unused = 70000000 - used
    additional_needed = 30000000 - unused
    debug_print(f"{used=} {unused=} {additional_needed=}")
    return min(filter(lambda x: x >= additional_needed, g))


class str2(str):
    def regex_sub(self, pattern, repl):
        return str2(re.sub(pattern, repl, self))

    def removeprefix(self, __prefix: str) -> str:
        return str2(super().removeprefix(__prefix))

    def replace(self, __old: str, __new: str, __count: SupportsIndex = -1) -> str:
        return str2(super().replace(__old, __new, __count))

    def strip(self, __chars: str | None = None) -> str:
        return str2(super().strip(__chars))


def cancer():
    s = (
        str2(get_day(7, test))
        .removeprefix("$ cd /")
        .replace("$ ls", "[")
        .replace("$ cd ..", "]")
        .regex_sub("[$a-z.]", "")  # remove file/folder names and remaining '$'
        .strip()
        .regex_sub("\\[\\s*", "[")  # trim space before '['
        .regex_sub("\\s*]", "]")  # trim space after ']'
        .regex_sub("\\s+", ",")  # replace remaining whitespace with commas
    )

    s = "[" + s
    unmatched_count = s.count("[") - s.count("]")
    s += "]" * unmatched_count

    js = json.loads(s)
    folder_sizes = []

    def space_used(folder):
        if isinstance(folder, int):
            return folder
        sum_inside = sum(space_used(i) for i in folder)
        folder_sizes.append(sum_inside)
        return sum_inside

    additional_needed = space_used(js) - 40000000
    return (
        sum(filter(lambda x: x <= 100000, folder_sizes)),
        min(filter(lambda x: x >= additional_needed, folder_sizes)),
    )


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
    benchmark(cancer)
