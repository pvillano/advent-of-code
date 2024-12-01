from collections import Counter

from utils import benchmark, get_day, test


def parse(raw: str):
    ret = []
    for line in raw.splitlines():
        ret.append(line)
    return ret

ink = "1   2"
def part1(raw: str):
    ll, rr = [], []
    for line in ink.split('\n'):
        l, r = line.split("   ")
        l, r = int(l), int(r)
        ll.append(l)
        rr.append(r)
    ll.sort()
    rr.sort()
    s = 0
    for l,r in zip(ll,rr):
        s += abs(l - r)
    print(s)


def part2(raw: str):
    ll, rr = [], []
    for line in ink.split('\n'):
        l, r = line.split("   ")
        l, r = int(l), int(r)
        ll.append(l)
        rr.append(r)
    ll.sort()
    rr.sort()
    rr = Counter(rr)
    s = 0
    for l in ll:
        s += l * rr[l]
    print(s)


test1 = """"""

expected1 = None

test2 = test1
expected2 = None


print(part1(test1))
print(part2(test1))


# def main():
#     test(part1, test1, expected1)
#     raw = get_day(1, override=True)
#     benchmark(part1, raw)
#     test(part2, test2, expected2)
#     benchmark(part2, raw)
#
#
# if __name__ == "__main__":
#     main()
