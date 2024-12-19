__all__ = [
    "grid_index",
    "NEWS_RC",
    "NEWS_XY",
    "NESW_RC",
    "NESW_XY",
    "rotate_clockwise",
    "rotate_counterclockwise",
    "transpose",
]

from collections.abc import Collection, Reversible, Iterable

NEWS_RC = ((-1, 0), (0, 1), (0, -1), (1, 0))
NEWS_XY = ((0, 1), (1, 0), (-1, 0), (0, -1))
NESW_RC = ((-1, 0), (0, 1), (1, 0), (0, -1))
NESW_XY = ((0, 1), (1, 0), (0, -1), (-1, 0))


def transpose(iterable: Iterable[Collection]):
    iterable = list(iterable)
    assert len(set(map(len, iterable))) == 1, "Matrix must not be jagged"
    return list(map(list, zip(*iterable)))


def rotate_clockwise(grid: Reversible[Collection]):
    return transpose(reversed(grid))


def rotate_counterclockwise(grid: Iterable[Collection]):
    return reversed(transpose(grid))


def grid_index(grid, value):
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == value:
                return r, c
    raise ValueError(f"{value} is not in grid")
