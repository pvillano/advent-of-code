

data ="""..."""


test_data = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###"""


dragon = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
dragon = dragon.split("\n")


# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH

the_map = test_data.split("\n")
the_map = [list(line) for line in the_map]


def rotations(tile):
    # 8
    # TESTED
    ret = []
    for transpose in (False, True):
        for flip_hor in (False, True):
            for flip_vert in (False, True):
                new_tile = list(tile)
                if transpose:
                    jmax = len(tile)
                    imax = len(tile[0])
                    new_tile = []
                    for i in range(imax):
                        row = []
                        for j in range(jmax):
                            row.append(tile[j][i])
                        line = "".join(row)
                        new_tile.append(line)
                if flip_hor:
                    new_tile = [x[::-1] for x in new_tile]
                if flip_vert:
                    new_tile = new_tile[::-1]
                ret.append(new_tile)
    return ret

total_spotted = 0

map_height = len(the_map[0])
map_width = len(the_map)

for real_dragon in rotations(dragon):
    dragon_height = len(real_dragon[0])
    dragon_width = len(real_dragon)
    for x in range(0, map_width - dragon_width + 1):
        for y in range(0, map_height - dragon_height + 1):
            spotted = True
            for dx in range(dragon_width):
                for dy in range(dragon_height):
                    if real_dragon[dx][dy] == "#":
                        if not the_map[x+dx][y+dy] == "#" or the_map[x+dx][y+dy] == "O":
                            spotted = False
            if spotted:
                total_spotted+=1
                for dx in range(dragon_width):
                    for dy in range(dragon_height):
                        if real_dragon[dx][dy] == "#":
                            the_map[x + dx][y + dy] = "O"


print(total_spotted)
boop = 0
for line in the_map:
    for ch in line:
        if ch == "#":
            boop += 1
print(boop)

