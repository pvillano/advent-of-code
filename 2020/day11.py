from copy import deepcopy
from itertools import count

test_data = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

data = """..."""

lines = data.rstrip().split("\n")
start = [list(line) for line in lines]

empty = "L"
floor = "."
occupied = "#"

num_rows = height = len(start)
num_cols = width = len(start[0])

cur = deepcopy(start)
prev = [["."] * width for i in range(height)]

num_rounds = 0
while prev != cur:
    prev = cur
    cur = [["."] * width for i in range(height)]
    for row in range(height):
        for col in range(width):
            occupied_count = 0
            for r_off in [-1, 0, 1]:
                for c_off in [-1, 0, 1]:
                    if r_off == c_off == 0:
                        continue
                    for i in count(1):
                        r = row + r_off * i
                        c = col + c_off * i
                        if r < 0 or r >= num_rows or c < 0 or c >= num_cols:
                            break
                        if prev[r][c] == occupied:
                            occupied_count += 1
                            break
                        if prev[r][c] == empty:
                            break

            if prev[row][col] == empty and occupied_count == 0:
                cur[row][col] = occupied
            elif prev[row][col] == occupied and occupied_count >= 5:
                cur[row][col] = empty
            else:
                cur[row][col] = prev[row][col]
    num_rounds += 1
    # print("\n".join("".join(row) for row in cur))
    # print()

print(sum(sum(1 for x in row if x == occupied) for row in cur))
