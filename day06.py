
from math import *
from itertools import *
from collections import *

children = defaultdict(list)
with open('day06.txt') as f:
    for line in f:
        parent, child, = line.strip().split(')')
        children[parent].append(child)


def recurse(node, depth):
    return sum(recurse(child, depth + 1) for child in children[node]) + depth


print(recurse('COM', 0))
print(children['COM'])
