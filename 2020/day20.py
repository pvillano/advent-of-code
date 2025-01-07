





# all 10x10

# 144 tiles

# 3x12 or 2x72
from collections import defaultdict, Counter, namedtuple

data = """..."""

test_data = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

sides_to_id = defaultdict(list)
id_to_sides = defaultdict(list)

DEBUG = True

if DEBUG:
    data = test_data
    one44 = 9
    twelve = 3
else:
    pass
    one44 = 144
    twelve = 12


def cannonize(side):
    return min(side, side[::-1])


for tile in test_data.split("\n\n"):
    title_str, *lines = tile.split("\n")
    title = int(title_str[5:-1])
    four_edges = [  # top clockwise
        lines[0],
        "".join(row[-1] for row in lines),
        lines[-1][::-1],
        "".join([row[0]for row in lines][::-1]),
    ]
    for i in range(4):
        cannon_side = cannonize(four_edges[i])
        sides_to_id[cannon_side].append(title)
    id_to_sides[title] = tuple(four_edges)
#
# print("len sides to id", len(sides_to_id))
# sides_to_id_count = Counter(len(x) for x in sides_to_id.values())
# print(sides_to_id_count)
# print("len id to sides", len(id_to_sides))
# # for k, v in id_to_sides.items():
# #     print(k, len(v))
# print()
# for title, sides in id_to_sides.items():
#     unique_sides_count = 0
#     for side in sides:
#         cannon_side = min(side, side[::-1])
#         ids = sides_to_id[cannon_side]
#         if len(ids) == 1:
#             unique_sides_count+=1
#     if unique_sides_count > 1:
#         print(title, unique_sides_count)


def rotations(four_edges):
    s1,s2,s3,s4 = four_edges
    return [
        (s1,s2,s3,s4,),
        (s2,s3,s4,s1,),
        (s3,s4,s1,s2,),
        (s4,s1,s2,s3,),
        (s4[::-1],s3[::-1],s2[::-1],s1[::-1],),
        (s1[::-1],s4[::-1],s3[::-1],s2[::-1],),
        (s2[::-1],s1[::-1],s4[::-1],s3[::-1],),
        (s3[::-1],s2[::-1],s1[::-1],s4[::-1],),
    ]


map_tile = namedtuple("map_tile", "id sides")

free_ids = list(id_to_sides.keys())



map = [[map_tile(None, (None, None, None)) for j in range(twelve)] for i in range(twelve)]


del cannon_side, four_edges, data, i, lines, title, title_str

def recurse(i,):
    if i == one44:
        corner_ids = []
        tot = 1
        for x,y in ((0,0),(0,-1),(-1,0),(-1,-1)):
            title = map[x][y].id
            corner_ids.append(title)
            tot *= title
        print(corner_ids)
        print(tot)
        exit(0)
    y, x = divmod(i, twelve)
    # left_neighbour = (x-1,y)
    # upper_neighbour = (x,y-1)
    left_neighbour_right = False
    top_neighbour_bottom = False
    cand_ids = None
    if x-1 >= 0:  # deal with left neighbour
        left_neighbour = map[x-1][y]
        left_neighbour_right = left_neighbour.sides[1]
        lnr_cannon = cannonize(left_neighbour_right)
        cand_ids = [x for x in sides_to_id[lnr_cannon] if x in free_ids]
    if y-1 >= 0:
        top_neighbour = map[x][y-1]
        top_neighbour_bottom = top_neighbour.sides[2]
        tnb_cannon = cannonize(top_neighbour_bottom)
        my_cand_ids = [x for x in sides_to_id[tnb_cannon] if x in free_ids]
        if cand_ids is not None:
            cand_ids = [x for x in my_cand_ids if x in cand_ids]
        else:
            cand_ids = my_cand_ids

    if cand_ids is None:
        cand_ids = list(free_ids)
    if not cand_ids:
        return # fail

    for title in cand_ids:
        free_ids.remove(title)
        edges = id_to_sides[title]
        for rotation in rotations(edges):
            if left_neighbour_right:
                me_left = rotation[3][::-1]
                if me_left != left_neighbour_right:
                    continue
            if top_neighbour_bottom:
                me_top = rotation[0][::-1]
                if me_top != top_neighbour_bottom:
                    continue
            map[x][y] = map_tile(title, rotation)
            recurse(i+1)
        map[x][y] = map_tile(None, (None, None, None, None))
        free_ids.append(title)

recurse(0)