import inspect
import sys
from typing import Any

from .std import DEBUG

__all__ = ["debug_print", "debug_print_grid", "debug_print_sparse_grid", "debug_print_recursive"]


def debug_print(*args, override=False, **kwargs) -> None:
    """
    Passes arguments to `print`,
    if currently executing program
    is being debugged or override is True
    :param args: same as print
    :param override:
    :param kwargs: same as print
    :return:
    """
    if not (DEBUG or override):
        return
    return print(*args, **kwargs, file=sys.stderr, flush=True)


def debug_print_grid(grid, *, override=False) -> None:
    """

    :param grid:
    :param override:
    :return:
    """
    if not (DEBUG or override):
        return
    for line in grid:
        print(*line, file=sys.stderr, flush=True)
    print()


BASE_INDENT = len(inspect.stack()) + 1


def debug_print_recursive(*args, override=False, **kwargs) -> None:
    """

    :param args:
    :param override:
    :param kwargs:
    :return:
    """
    if not (DEBUG or override):
        return
    indent = len(inspect.stack()) - BASE_INDENT
    return print(" |" * indent, *args, **kwargs, file=sys.stderr, flush=True)


def debug_print_sparse_grid(
        grid_map: dict[(int, int), Any] or set, *, transpose=False, override=False
) -> None:
    """

    :param grid_map:
    :param transpose:
    :param override:
    :return:
    """
    if not (DEBUG or override):
        return
    if isinstance(grid_map, set):
        grid_map = {k: "# " for k in grid_map}
    x0, x1 = min(k[0] for k in grid_map.keys()), max(k[0] for k in grid_map.keys())
    y0, y1 = min(k[1] for k in grid_map.keys()), max(k[1] for k in grid_map.keys())
    max_w = max(len(str(v)) for v in grid_map.values())
    if not transpose:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if (x, y) in grid_map:
                    print(
                        str(grid_map[(x, y)]).rjust(max_w + 1), end="", file=sys.stderr
                    )
                else:
                    print(" " * max_w, end=" ", file=sys.stderr)
            print(file=sys.stderr, flush=True)
    else:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x, y) in grid_map:
                    print(
                        str(grid_map[(x, y)]).rjust(max_w + 1), end="", file=sys.stderr
                    )
                else:
                    print(" " * max_w, end=" ", file=sys.stderr)
            print(file=sys.stderr, flush=True)
    print(file=sys.stderr, flush=True)
