__all__ = ["rotations", "flatten", "degenerate"]

from collections.abc import Iterable, Callable
from itertools import chain
from typing import Iterator

from utils.grids import transpose


def rotations(iterable: Iterable):
    iterable = tuple(iterable)
    for idx in range(len(iterable)):
        yield tuple(chain(iterable[-idx:], iterable[:-idx]))


flatten = chain.from_iterable


def degenerate[**I, O](user_function: Callable[I, Iterator[O]]) -> Callable[I, list[O]]:
    """
    Turns a generator into a function which returns a list
    :param user_function:
    :return:
    """
    def wrapper(*args, **kw):
        return list(user_function(*args, **kw))

    wrapper.__name__ = user_function.__name__
    wrapper.__dict__ = user_function.__dict__
    wrapper.__doc__ = user_function.__doc__
    return wrapper


def main():
    @degenerate
    def range_list(start, stop=None, step=None):
        if stop is None:
            r = range(start)
        elif step is None:
            r = range(start, stop)
        else:
            r = range(start, stop, step)
        for i in r:
            yield i

    assert range_list(10) == list(range(10))

    l = [[10 * x + y for y in range(10)] for x in range(20)]
    lt = transpose(l)
    for i, line in enumerate(lt):
        for j, val in enumerate(line):
            assert val == l[j][i]


if __name__ == "__main__":
    main()
