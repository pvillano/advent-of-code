from itertools import product, chain


flatten = chain.from_iterable

data = """..."""

test_data = """.#.
..#
###"""

ON = "#"
OFF = "."

lines = data.split("\n")

width = len(lines[0])
height = len(lines)

# max_dim = max(width, height) + 20
#
# def make_map():
#     return [[["." for k in range(max_dim)] for j in range(max_dim)] for i in range(max_dim)]
#
# old_map = make_map()
# new_map = make_map()
#
#
# for i in range(height):
#     for j in range(width):
#         for k in (max_dim//2,):
#             i_map = i + (max_dim - height)//2
#             j_map = j + (max_dim - width)//2
#             old_map[i_map][j_map][k] = lines[i][j]
#
#
# print(sum(1 for ch in flatten(flatten(old_map)) if ch == ON))
#
# for generation in range(6):
#     for i, j, k in product(range(1, max_dim - 1),range(1, max_dim - 1),range(1, max_dim - 1)):
#         active = old_map[i][j][k]
#         neighbours_on = 0
#         for di, dj, dk in product((-1,0,1),(-1,0,1),(-1,0,1)):
#             if old_map[i+di][j+dj][k+dk] == ON:
#                 neighbours_on += 1
#         if active == ON:
#             neighbours_on -= 1
#             if neighbours_on in (2,3):
#                 new_map[i][j][k] = ON
#             else:
#                 new_map[i][j][k] = OFF
#         else:
#             if neighbours_on == 3:
#                 new_map[i][j][k] = ON
#             else:
#                 new_map[i][j][k] = OFF
#     print(sum(1 for ch in flatten(flatten(new_map)) if ch == ON))
#     old_map, new_map = new_map, old_map


max_dim = max(width, height) + 20


def make_map():
    return [[[["." for w in range(max_dim)] for k in range(max_dim)] for j in range(max_dim)] for i in range(max_dim)]


old_map = make_map()
new_map = make_map()

for i, j, k, w in product(range(height), range(width), (max_dim // 2,), (max_dim // 2,)):
    i_map = i + (max_dim - height) // 2
    j_map = j + (max_dim - width) // 2
    old_map[i_map][j_map][k][w] = lines[i][j]

for generation in range(6):
    for i, j, k, w in product(range(1, max_dim - 1), range(1, max_dim - 1), range(1, max_dim - 1),range(1, max_dim - 1)):
        active = old_map[i][j][k][w] == ON
        neighbours_on = 0
        for di, dj, dk, dw in product((-1, 0, 1), (-1, 0, 1), (-1, 0, 1), (-1, 0, 1)):
            if old_map[i + di][j + dj][k + dk][w + dw] == ON:
                neighbours_on += 1
        if active:
            neighbours_on -= 1
            if neighbours_on in (2, 3):
                new_map[i][j][k][w] = ON
            else:
                new_map[i][j][k][w] = OFF
        else:
            if neighbours_on == 3:
                new_map[i][j][k][w] = ON
            else:
                new_map[i][j][k][w] = OFF
    tot_on = sum(1 for ch in flatten(flatten(flatten(new_map))) if ch == ON)
    old_map, new_map = new_map, old_map
