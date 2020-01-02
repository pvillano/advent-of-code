from math import *
from itertools import *


def double(input):
    for c1, c2 in zip(input, input[1:],):
        if c1 == c2:
            return True
    return False


def inc(input):
    for c1, c2 in zip(input, input[1:]):
        if int(c1) > int(c2):
            return False
    return True

answer = 0
for i in range(123257, 647015):
    str_i = str(i).zfill(6)
    if double(str_i) and inc(str_i):
        answer += 1

print(answer)
