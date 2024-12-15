from copy import deepcopy
from itertools import product

from utils import get_day, test, benchmark
from utils.grids import NEWS_RC
from utils.printing import debug_print_grid, debug_print

to_dr_dc = {k: v for k, v in zip("^><v", NEWS_RC)}


def parse(raw: str):
    atlas, moves = raw.split('\n\n')
    atlas = atlas.splitlines()
    r, c = 0, 0
    for r, row in enumerate(atlas):
        if (c := row.find('@')) >= 0:
            break
    atlas = [[ch for ch in rows] for rows in atlas]

    moves = list(filter(lambda x: x in "<v>^", moves))
    return r, c, atlas, moves


def part1(raw: str):
    wall = '#'
    box = 'O'
    r, c, atlas, moves = parse(raw)
    height, width = len(atlas), len(atlas[0])
    for move in moves:
        debug_print_grid(atlas)
        assert atlas[r][c] == '@'
        dr, dc = to_dr_dc[move]
        nr, nc = r + dr, c + dc
        if atlas[nr][nc] == '.':
            atlas[r][c], atlas[nr][nc] = atlas[nr][nc], atlas[r][c]
            r, c = nr, nc
            continue
        if atlas[nr][nc] == '#':
            continue
        assert atlas[nr][nc] == box
        while nr in range(height) and nc in range(width) and atlas[nr][nc] == box:
            nr += dr
            nc += dc
        if nr not in range(height) or nc not in range(width) or atlas[nr][nc] == wall:
            # unmovable
            continue
        # else movable
        assert atlas[nr][nc] == '.'
        assert atlas[r][c] == '@'
        atlas[nr][nc] = box
        atlas[r][c] = '.'
        r, c = r + dr, c + dc
        atlas[r][c] = '@'
    s = 0
    for r, c in product(range(height), range(width)):
        if atlas[r][c] == box:
            s += 100 * r + c
    return s


expand = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@.",
}


def parse2(raw: str):
    atlas, moves = raw.split('\n\n')
    atlas = atlas.splitlines()

    def xpand(row):
        for ch in row:
            yield from expand[ch]

    atlas = [list(xpand(row)) for row in atlas]
    r, c = 0, 0
    found = False
    for r, row in enumerate(atlas):
        for c, ch in enumerate(row):
            if ch == '@':
                found = True
                break
        if found:
            break
    assert found
    moves = list(filter(lambda x: x in "<v>^", moves))
    return r, c, atlas, moves


def part2(raw: str):
    box = '[]'
    r, c, atlas, moves = parse2(raw)
    debug_print_grid(atlas)
    height, width = len(atlas), len(atlas[0])
    for move in moves:
        debug_print(move)
        debug_print_grid(atlas)
        assert atlas[r][c] == '@'
        dr, dc = to_dr_dc[move]
        nr, nc = r + dr, c + dc
        if atlas[nr][nc] == '.':
            atlas[r][c], atlas[nr][nc] = atlas[nr][nc], atlas[r][c]
            r, c = nr, nc
            assert atlas[r][c] == '@'
            continue
        if atlas[nr][nc] == '#':
            assert atlas[r][c] == '@'
            continue

        assert atlas[nr][nc] in box

        if move in '<>':
            while nr in range(height) and nc in range(width) and atlas[nr][nc] in '[]':
                nr += dr
                nc += dc
            if nr not in range(height) or nc not in range(width) or atlas[nr][nc] == '#':
                # unmovable
                continue
            # else movable
            assert atlas[nr][nc] == '.'
            assert atlas[r][c] == '@'
            # atlas[r][r+dr:nr] = atlas[c][r:nr-dr]
            if move == '<':
                oldstart, oldend = nc - dc, c
                newstart, newend = nc, c + dc
            else:
                oldstart, oldend = c, nc
                newstart, newend = c + dc, nc + dc
            atlas[r][newstart:newend] = atlas[r][oldstart:oldend]
            atlas[r][c] = '.'
            r, c = r + dr, c + dc
            atlas[r][c] = '@'
        else:
            q = [(nr, nc)]
            seen = set()
            blocked = False
            while q and not blocked:
                check_r, check_c = q.pop()
                if (check_r, check_c) in seen:
                    continue
                if atlas[check_r][check_c] == '.':
                    continue
                if atlas[check_r][check_c] == '#':
                    blocked = True
                    break
                assert atlas[check_r][check_c] in '[]'
                seen.add((check_r, check_c))
                if atlas[check_r][check_c] == '[':
                    q.append((check_r, check_c + 1))
                if atlas[check_r][check_c] == ']':
                    q.append((check_r, check_c - 1))
                q.append((check_r + dr, check_c + dc))

            if blocked:
                continue
            else:
                new_atlas = deepcopy(atlas)
                for rr, cc in seen:
                    new_atlas[rr][cc] = '.'
                for rr, cc in seen:
                    new_atlas[rr + dr][cc + dc] = atlas[rr][cc]
                atlas = new_atlas
                assert atlas[r][c] == '@'
                assert atlas[nr][nc] == '.'
                atlas[r][c], atlas[nr][nc] = atlas[nr][nc], atlas[r][c]
                r, c = nr, nc

    debug_print_grid(atlas, override=True)

    s = 0
    for r, c in product(range(height), range(width)):
        if atlas[r][c] == '[':
            s += 100 * r + c
    return s


test1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

expected1 = 2028

test11 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

expected11 = 10092

test2 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""
expected2 = 9021


def main():
    # test(part1, test1, expected1)
    raw = get_day(15)
    # benchmark(part1, raw)
    test(part2, test11, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
