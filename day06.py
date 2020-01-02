
from math import *
from itertools import *
from collections import *

children = defaultdict(list)
with open('day06.txt') as f:
    for line in f:
        parent, child, = line.strip().split(')')
        children[parent].append(child)


def recurse_person(node, person):
    if person in children[node]:
        return 1
    for i in (recurse_person(child, person) for child in children[node]):
        if i:
            return i + 1
    return False

def recurse(node, depth):
    for i in (recurse(child, depth + 1) for child in children[node]):
        if i:
            return i
    if not children[node]:
        return 0
    d_you = max(recurse_person(child, 'YOU') for child in children[node])
    d_san = max(recurse_person(child, 'SAN') for child in children[node])
    if d_you and d_san:
        return d_you + d_san
    else:
        return 0




print(recurse('COM', 0))
