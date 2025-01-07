from itertools import count

data = """..."""

test_data = """5764801
17807724"""

lines = test_data.split("\n")

card, door = map(int, lines)

card_i = 1
for i in count(1):
    card_i = (card_i * 7) % 20201227
    if card_i == card:
        break

door_j = 1
for j in count(1):
    door_j = (door_j * 7) % 20201227
    if door_j == door:
        break

print(i, j)

out_i = 1
for k in range(j):
    out_i = (out_i * card) % 20201227
out_j = 1
for k in range(i):
    out_j = (out_j * door) % 20201227
print(out_i, out_j)
