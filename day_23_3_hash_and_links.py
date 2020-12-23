
from itertools import count, islice, chain

from otqdm import otqdm

data = """..."""

test_data = """389125467"""

# AAAAAAAAAAAAH
cups_list = list(map(int, list(test_data)))

cups_map = {}
for k, v in zip(chain([1000000], cups_list, range(len(cups_list)+1, 1000000)),chain(cups_list, range(len(cups_list)+1, 1000000+1))):
    cups_map[k] = v

# for k,v in zip(cups_list, cups_list[1:] + cups_list[0:1]):
#     cups_map[k] = v

cur_cup = cups_list[0]
for i in otqdm(range(10000000)):

    rem = cur_cup
    removed = []
    for j in range(3):
        rem = cups_map[rem]
        removed.append(rem)
    dest_cup = (cur_cup - 2) % len(cups_map) + 1
    while dest_cup in removed:
        dest_cup -= 1
        dest_cup = (dest_cup - 1) % len(cups_map) + 1

    gap = (cur_cup, cups_map[removed[-1]])
    l_join = (dest_cup, removed[0])
    r_join = (removed[-1], cups_map[dest_cup])

    for k, v in (gap, l_join, r_join):
        cups_map[k] = v

    cur_cup = cups_map[cur_cup]


c1 = cups_map[1]
c2 = cups_map[c1]

print(c1, c2, c1*c2)
