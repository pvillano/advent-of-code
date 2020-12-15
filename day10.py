from itertools import product, count, cycle
from math import gcd

test_data = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

data = """..."""


asteroid_map = data.split('\n')

num_rows = len(asteroid_map)
num_cols = len(asteroid_map[0])

def visible(r1, c1, r2, c2):
    dr, dc = (r2 - r1), (c2 - c1)
    gcd2 = gcd(dr, dc)

    dr, dc = dr//gcd2, dc//gcd2
    for i in range(1, gcd2):
        if asteroid_map[r1 + i * dr][c1 + i * dc] == "#":
            return False
    return True


num_visible = [[0] * num_cols for i in range(num_rows)]
for station_row, station_col in product(range(num_rows), range(num_cols)):
    if asteroid_map[station_row][station_col] != '#':
        continue
    for asteroid_row, asteroid_col in product(range(num_rows), range(num_cols)):
        if asteroid_map[asteroid_row][asteroid_col] != '#':
            continue
        if (station_row, station_col) == (asteroid_row, asteroid_col):
            continue
        if visible(station_row, station_col, asteroid_row, asteroid_col):
            num_visible[station_row][station_col] += 1


best = max(*[max(*row) for row in num_visible])
for station_row, station_col in product(range(num_rows), range(num_cols)):
    if num_visible[station_row][station_col] == best:
        print(station_row, station_col)
        break

print(best)

num_rows = len(asteroid_map)
num_cols = len(asteroid_map[0])

def visible(r1, c1, r2, c2):
    dr, dc = (r2 - r1), (c2 - c1)
    gcd2 = gcd(dr, dc)

    dr, dc = dr//gcd2, dc//gcd2
    for i in range(1, gcd2):
        if asteroid_map[r1 + i * dr][c1 + i * dc] == "#":
            return False
    return True

def simplify(frac):
    num, denom = frac
    divisor = gcd(num, denom)
    return num//divisor, denom//divisor

def in_bounds(r, c):
    return 0 <= r < num_rows and 0 <= c < num_cols

max_fract = max(num_rows, num_cols)

fracts = map(simplify, product(range(max_fract), range(1, max_fract)))
fracts = list(set(fracts))
fracts = sorted(set(fracts), key=lambda x: x[0]/x[1])
print(fracts)
slopes = [(x, -y) for x, y in fracts] + [(y, x) for x, y in fracts] + [(-x, y) for x, y in fracts] + [(-y, -x) for x, y in fracts]

my_map = [list(row) for row in asteroid_map]

i = 0
for x, y in cycle(slopes):
    for j in count(1):
        asteroid_row = station_row + j * y
        asteroid_col = station_col + j * x
        if not in_bounds(asteroid_row, asteroid_col):
            break
        if my_map[asteroid_row][asteroid_col] == "#":
            my_map[asteroid_row][asteroid_col] = '.'
            if i+1 in (1,2,3,10,20,50,100,199,200):
                print(asteroid_col, asteroid_row, asteroid_col*100 + asteroid_row)
            i += 1
            break
    if i == 200:
        break



