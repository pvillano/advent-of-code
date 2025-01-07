





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
title_to_data = defaultdict(list)

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


for tile in data.split("\n\n"):
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
    title_to_data[title] = lines


def rotations(tile):
    # 8
    # WORKS
    ret = []
    width = len(tile)
    for transpose in (False, True):
        for flip_hor in (False, True):
            for flip_vert in (False, True):
                new_tile = list(tile)
                if transpose:
                    new_tile = ["".join(tile[j][i] for j in range(width)) for i in range(width)]
                if flip_hor:
                    new_tile = [x[::-1] for x in new_tile]
                if flip_vert:
                    new_tile = new_tile[::-1]
                ret.append(new_tile)
    return ret



free_ids = list(title_to_data.keys())

id_map = [[None for j in range(twelve)] for i in range(twelve)]
tile_map = [[None for j in range(twelve)] for i in range(twelve)]

final_map = None
del cannon_side, four_edges, data, i, lines, title, title_str

def recurse(i,):
    # if i == 3:
    #     print()
    if i == one44:
        corner_ids = []
        tot = 1
        for x,y in ((0,0),(0,-1),(-1,0),(-1,-1)):
            title = id_map[x][y]
            corner_ids.append(title)
            tot *= title
        # print(corner_ids)
        # print(tot)
        out = []
        for x in range(twelve):
            for inner_y in range(1,9):
                line = []
                for y in range(twelve):
                    line.append(tile_map[y][x][inner_y][1:-1])
                line = "".join(line)
                out.append(line)

        for line in out:
            print(line)
        exit()

    y, x = divmod(i, twelve)
    left_neighbour_right = False
    top_neighbour_bottom = False
    cand_ids = None
    if x-1 >= 0:  # deal with left neighbour
        left_neighbour = tile_map[x-1][y]
        left_neighbour_right = "".join(row[-1] for row in left_neighbour)
        lnr_cannon = cannonize(left_neighbour_right)
        cand_ids = [x for x in sides_to_id[lnr_cannon]]
    if y-1 >= 0:
        top_neighbour = tile_map[x][y-1]
        top_neighbour_bottom = top_neighbour[-1]
        tnb_cannon = cannonize(top_neighbour_bottom)
        my_cand_ids = [x for x in sides_to_id[tnb_cannon]]
        if cand_ids is not None:
            cand_ids = [x for x in my_cand_ids if x in cand_ids]
        else:
            cand_ids = my_cand_ids

    if cand_ids is None:
        cand_ids = list(free_ids)
    if not cand_ids:
        return # fail

    for title in cand_ids:
        if any(title in row for row in id_map):
            continue
        id_map[x][y] = title
        tile = title_to_data[title]
        for rotation in rotations(tile):
            if left_neighbour_right:
                me_left = "".join([row[0]for row in rotation])
                if me_left != left_neighbour_right:
                    continue
            if top_neighbour_bottom:
                me_top = rotation[0]
                if me_top != top_neighbour_bottom:
                    continue
            tile_map[x][y] = rotation
            recurse(i+1)
        id_map[x][y] = None
        tile_map[x][y] = None
        # free_ids.append(title)

recurse(0)