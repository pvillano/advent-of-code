import operator
from collections import defaultdict, deque, Counter
from copy import copy, deepcopy
from functools import cache, lru_cache, partial, reduce
from itertools import (
    accumulate,
    count,
    cycle,
    product,
    permutations,
    combinations,
    pairwise,
    islice
)
from math import sqrt, floor, ceil, gcd, sin, cos, atan2

from otqdm import otqdm

from utils import benchmark, debug_print, get_day, pipe, debug_print_grid

rocks_raw = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""
test = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
raw = get_day(17, test)


def overlaps(x, y, rock, stack: deque[str]):
    """
    top left corner of stack is 0,0
    bottom left corner of rock starts at 2,4

    """
    for dx, dy in rock:
        xx, yy = x + dx, y + dy
        row, column = -yy, xx
        if column not in range(7):
            return "side"
        if row in range(len(stack)):
            if stack[row][column] == '#':
                return "bottom"
    return "safe"


def parse_rocks():
    rock_strs = rocks_raw.split("\n\n")
    rocks = []
    for rock_str in rock_strs:
        rock = []
        lines = rock_str.split('\n')
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '#':
                    x, y = col, len(lines) - row - 1
                    rock.append((x, y))
        assert (0, 1) in rock or (1, 0) in rock
        rocks.append(rock)
    return rocks


def add_rock(x, y, rock, stack: deque[str]):
    lines_added = 0
    rows = [['.'] * 7 for _ in range(4)]
    for dx, dy in rock:
        xx, yy = x+dx, y+dy
        row, col = y+dy-1,x+dx
        if yy <= 0:
            old = list(stack[-yy])
            old[xx] = '#'
            stack[-yy] = "".join(old)
        else:
            rows[row][col] = '#'
    # assert '#' in rows[0]
    for row in rows:
        s = "".join(row)
        stack.appendleft(s)
        lines_added += 1
    while stack[0] == '.......':
        stack.popleft()
        lines_added -= 1
    return lines_added


def part1():
    rocks = parse_rocks()

    lr_to_i = {'<': -1, '>': 1}

    moves = cycle(raw)
    cave: deque[str] = deque(maxlen=100)
    cave.appendleft("#######")
    total_height = 0
    for idx, rock in zip(range(2022), cycle(rocks)):
        # debug_print("The", idx+1 ,"rock begins falling:")
        # bottom left
        if idx == 4:
            pass
        x, y = 2, 4
        while True:
            # try moving right/left
            next_move = next(moves)
            new_x, new_y = x + lr_to_i[next_move], y
            overlap = overlaps(new_x, new_y, rock, cave)
            if overlap == "safe":
                debug_print("Jet of gas pushes rock", next_move)
                x, y = new_x, new_y
            else:
                pass
                debug_print("Jet of gas pushes rock", next_move, ", but nothing happens")

            new_x, new_y = x, y - 1
            overlap = overlaps(new_x, new_y, rock, cave)

            if overlap == "bottom":
                debug_print("Rock falls 1 unit, causing it to come to rest")
                total_height += add_rock(x, y, rock, cave)
                debug_print_grid(cave)
                break
            else:
                debug_print("Rock falls 1 unit")
                x, y = new_x, new_y
    return total_height


def hash_state(rock_idx, moves_idx, stack, view=300):
    return f"{rock_idx},{moves_idx},{''.join(islice(stack, view))}"


def part2():
    alot = 1000000000000
    rocks = parse_rocks()

    lr_to_i = {'<': -1, '>': 1}

    move_idx = -1
    cave: deque[str] = deque(maxlen=1000)
    cave.appendleft("#######")
    total_height = 0
    history = dict()
    for num_fallen, rock_idx in zip(range(alot), cycle(range(len(rocks)))):

        state_hash = hash_state(rock_idx, move_idx, cave)
        if state_hash in history:
            old_num_fallen, old_total_height = history[state_hash]
            d_fallen = num_fallen - old_num_fallen
            d_height = total_height - old_total_height
            remaining_fallen = alot - num_fallen
            if remaining_fallen % d_fallen == 0:
                cycles = remaining_fallen//d_fallen
                return total_height + cycles * d_height
        elif num_fallen > 1000:
            history[state_hash] = num_fallen, total_height
        # debug_print("The", idx+1 ,"rock begins falling:")
        # bottom left
        rock = rocks[rock_idx]
        x, y = 2, 4
        while True:
            # try moving right/left
            move_idx = (move_idx + 1) % len(raw)
            next_move = raw[move_idx]
            new_x, new_y = x + lr_to_i[next_move], y
            overlap = overlaps(new_x, new_y, rock, cave)
            if overlap == "safe":
                # debug_print("Jet of gas pushes rock", next_move)
                x, y = new_x, new_y
            else:
                pass
                # debug_print("Jet of gas pushes rock", next_move, ", but nothing happens")

            new_x, new_y = x, y - 1
            overlap = overlaps(new_x, new_y, rock, cave)

            if overlap == "bottom":
                # debug_print("Rock falls 1 unit, causing it to come to rest")
                total_height += add_rock(x, y, rock, cave)
                # debug_print_grid(cave)
                break
            else:
                # debug_print("Rock falls 1 unit")
                x, y = new_x, new_y

    return total_height

if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
