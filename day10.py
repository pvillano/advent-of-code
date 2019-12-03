
from math import *
from itertools import *


with open('day10.txt') as f:
    for line in f:
        for token in line.split(', '):
            answer = token
            
print(answer)
