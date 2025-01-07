import time
from collections import defaultdict

start_time = time.time()

data = """..."""

test_data = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

lines = test_data.split("\n")

mappings = {
    "nw": "↖",
    "ne": "↗",
    "se": "↘",
    "sw": "↙",
}

to_dxdy = {
    "↖": (-1, 1),
    "↗": (0, 1),
    "↘": (1, -1),
    "↙": (0, -1),
    "w": (-1, 0),
    "e": (1, 0),
}

tiles = defaultdict(bool)  # black=True

for line in lines:
    for old, new in mappings.items():
        line = line.replace(old, new)
    cur_x, cur_y = 0, 0
    for token in line:
        dx, dy = to_dxdy[token]
        cur_x += dx
        cur_y += dy
    tiles[cur_x, cur_y] = not tiles[cur_x, cur_y]

print(sum(tiles.values()))

for i in range(100):
    num_adj = defaultdict(int)
    for k in tiles.keys():
        num_adj[k] = 0
    for (x, y), adj_cnt in tiles.items():
        if adj_cnt:
            for dx, dy in to_dxdy.values():
                num_adj[x + dx, y + dy] += 1
    for (x, y), adj_cnt in num_adj.items():
        if tiles[x, y]:
            if adj_cnt == 0 or adj_cnt > 2:
                tiles[x, y] = False
        else:
            if adj_cnt == 2:
                tiles[x, y] = True

print(sum(tiles.values()))


end_time = time.time()

print(end_time - start_time)