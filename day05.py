from collections import deque

from utils import benchmark, debug_print, get_day, DEBUG

test = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

initial, moves = get_day(5, test, override=True).split("\n\n")


def part1():
    nine = 9
    # if DEBUG:
    #     nine = 3
    tot = 0
    stacks = [deque() for _ in range(nine)]
    for line in initial.split('\n')[:-1]:
        for i in range(nine):
            idx = 1 + 4 * i
            c = line[idx]
            if c != ' ':
                stacks[i].appendleft(c)
    for s in stacks:
        debug_print(s)
    line: str
    for line in moves.rstrip('\n').split('\n'):
        count, from_stack, to_stack = map(int, line.lstrip("move ").replace(" from ", " to ").split(" to "))
        from_stack -= 1
        to_stack -= 1
        debug_print(count, from_stack, to_stack)
        for i in range(count):
            temp = stacks[from_stack].pop()
            stacks[to_stack].append(temp)

        for s in stacks:
            debug_print(s)
        debug_print()
    return "".join(s.pop() for s in stacks)


def part2():
    nine = 9
    # if DEBUG:
    #     nine = 3
    tot = 0
    stacks = [deque() for _ in range(nine)]
    for line in initial.split('\n')[:-1]:
        for i in range(nine):
            idx = 1 + 4 * i
            c = line[idx]
            if c != ' ':
                stacks[i].appendleft(c)
    for s in stacks:
        debug_print(s)
    line: str
    for line in moves.rstrip('\n').split('\n'):
        count, from_stack, to_stack = map(int, line.lstrip("move ").replace(" from ", " to ").split(" to "))
        from_stack -= 1
        to_stack -= 1
        debug_print(count, from_stack, to_stack)
        temp = deque()
        for i in range(count):
            temp.append(stacks[from_stack].pop())
        for i in range(count):
            stacks[to_stack].append(temp.pop())

        for s in stacks:
            debug_print(s)
        debug_print()
    return "".join(s.pop() for s in stacks)


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
