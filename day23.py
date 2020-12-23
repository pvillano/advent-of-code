from itertools import count, islice

from otqdm import otqdm

data = """..."""

test_data = """389125467"""


cups = list(map(int, list(test_data)))
num_cups = len(cups)

for i in range(100):
    removed = cups[1:4]
    cups = [cups[0]] + cups[4:]
    for j in range(1, num_cups):
        try:
            idx = cups.index((cups[0] - j) % (num_cups+1))
            cups = cups[:idx+1] + removed + cups[idx+1:]
            cups = cups[1:] + [cups[0]]
            break
        except ValueError:
            continue
    # print(cups)
idx1 = cups.index(1)
print(" ".join(map(str, list(cups[idx1+1:] + cups[:idx1]))))

# not

def gen():
    cups = list(map(int, list(data))) + list(range(len(list(data)), 1000001))
    for i in range(10000000):
        tup_cups = tuple(cups)
        yield tup_cups
        removed = cups[1:4]
        cups = [cups[0]] + cups[4:]
        for j in range(1, num_cups):
            try:
                idx = cups.index((cups[0] - j) % (num_cups+1))
                cups = cups[:idx+1] + removed + cups[idx+1:]
                cups = cups[1:] + [cups[0]]
                break
            except ValueError:
                continue


def solve():
    lgen = gen()
    for i, left, right in otqdm(zip(count(), lgen, islice(gen(), 0, None, 2)), len_iterator=10000000):
        if left == right and i != 0:
            diff = i
            remainder = (10000000 % diff)
            cups = left
            for j in range(remainder):
                cups = next(lgen)
            l, r = list(cups[idx1 + 1:] + cups[:idx1])[:2]
            print(l * r)
            exit(0)

if __name__ == '__main__':
    solve()
