from collections import deque
from itertools import count, islice

from otqdm import otqdm

data = """..."""

test_data = """389125467"""


cups = list(map(int, list(test_data)))
num_cups = len(cups)


cups = list(map(int, list(data))) + [range(len(list(data))+1, 100001),]
for i in otqdm(range(10000000)):
    # tup_cups = tuple(cups)
    # yield tup_cups
    for j in range(4):
        if isinstance(cups[j], int):
            pass
        else:
            start, stop = cups[j].start, cups[j].stop
            insert = start
            start += 1
            if stop - start > 1:
                cups = cups[:j] + [insert, range(start, stop)] + cups[j+1:]
            elif stop - start == 1:
                cups = cups[:j] + [insert, insert + 1] + cups[j + 1:]

    removed = cups[1:4]
    cups = [cups[0]] + cups[4:]
    dest_cup = cups[0] - 1
    while dest_cup in removed:
        dest_cup -= 1
        dest_cup = (dest_cup - 1) % 100000 + 1
    for j, cup in enumerate(cups):
        if cup == dest_cup:
            cups = cups[:j+1] + removed + cups[j+1:]
            break
        elif isinstance(cup, range)  and dest_cup in cup:
            left, right = range(cup.start, dest_cup-1), range(dest_cup+1, cup.stop)
            if not left:
                left = []
            elif len(left) == 1:
                left = list(left)
            else:
                left = [left]
            if not right:
                right = []
            elif len(right)==1:
                right = list(right)
            else:
                right = [right]
            cups = cups[:j] + left + [dest_cup] + removed + right + cups[j+1:]
            break
idx1 = cups.index(1)
l, r = list(cups[idx1 + 1:] + cups[:idx1])[:2]
print(l,r)
print(l * r)
print(cups)




# def solve():
#     lgen = gen()
#     for i, left, right in otqdm(zip(count(), lgen, islice(gen(), 0, None, 2)), len_iterator=10000000):
#         if left == right and i != 0:
#             diff = i
#             remainder = (10000000 % diff)
#             cups = left
#             for j in range(remainder):
#                 cups = next(lgen)
#             l, r = list(cups[idx1 + 1:] + cups[:idx1])[:2]
#             print(l * r)
#             exit(0)

# if __name__ == '__main__':
#     solve()
