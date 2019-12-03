
from math import *
from itertools import *

dirs = {
    'L': (-1, 0),
    'R': (1,0),
    'U': (0,1),
    'D': (0,-1),
}


with open('day03.txt') as f:
    lines = list(f)
    curpt = [0,0]
    pts = []
    for token in lines[0].split(','):
        direction = token[0]
        dist = int(token[1:])
        for i in range(dist):
            curpt[0] += dirs[direction][0]
            curpt[1] += dirs[direction][1]
            pts.append(tuple(curpt))
    pts = set(pts)


    curpt = [0,0]
    best = (10**10,0)
    for token in lines[1].split(','):
        direction = token[0]
        dist = int(token[1:])
        for i in range(dist):
            curpt[0] += dirs[direction][0]
            curpt[1] += dirs[direction][1]
            my = tuple(curpt)
            if my in pts:
                if sum(map(abs, my)) < sum(map(abs, best)):
                    best = my
                    print(best, sum(map(abs, best)))



