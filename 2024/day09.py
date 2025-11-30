from itertools import batched, islice

from utils import benchmark, get_input, test


def part1(raw: str):
    blocks = list(map(int, raw))

    def w_free_iter(b):
        for idx, bf in enumerate(batched(b, 2)):
            block, free = bf[0], (bf[1] if len(bf) == 2 else None)
            for _ in range(block):
                yield idx
            if free is not None:
                for _ in range(free):
                    yield None

    beelocks = list(w_free_iter(blocks))
    i = 0
    j = len(beelocks) - 1
    s = 0
    while i <= j:
        # assert i and j are unused
        if beelocks[i] is not None:
            s += i * beelocks[i]
            i += 1
        elif beelocks[j] is not None:
            assert beelocks[i] is None
            s += i * beelocks[j]
            i += 1
            j -= 1
        else:
            j -= 1
    return s


def part2(raw: str):
    blocks = list(map(int, raw))

    def w_free_iter(b):
        for idx, bf in enumerate(batched(b, 2)):
            block, free = bf[0], (bf[1] if len(bf) == 2 else None)
            yield [idx, block]
            if free is not None:
                yield [None, free]

    memory = list(w_free_iter(blocks))
    last_id = memory[-1][0]
    trial = -1
    for bid in reversed(range(last_id + 1)):
        try:
            while memory[trial][0] != bid:
                trial -= 1
            bid, size = memory[trial]
        except IndexError:
            break
        assert bid is not None
        action_idx = -1
        for i, (nun, free_size) in islice(enumerate(memory), 1, None, 2):
            assert nun is None
            if free_size >= size:
                action_idx = i
                break
        if action_idx == -1 or action_idx > len(memory) + trial:
            continue
        used, remaining = size, memory[action_idx][1] - size

        # [9,3] into [[None,4]] is [[None,0],[9,3],[None,1]]
        memory[action_idx] = [None, remaining]
        memory.insert(action_idx, [bid, size])
        memory.insert(action_idx, [None, 0])

        assert memory[trial - 1][0] is None
        # try:
        memory[trial - 1][1] += size
        memory[trial][1] = 0
        # except IndexError:
        #     break

    page = 0
    s = 0

    for id_or_none, size in memory:
        if id_or_none is None:
            page += size
        else:
            for _ in range(size):
                s += id_or_none * page
                page += 1
    return s


test1 = """2333133121414131402"""

expected1 = 1928

test2 = test1
expected2 = 2858


def main():
    test(part1, test1, expected1)
    raw = get_input(__file__)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
