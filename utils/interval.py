import collections
from collections.abc import Iterable


def range_overlaps(a: range, b: range):
    return a.start < b.stop and b.start < a.stop


class IntervalSet(collections.abc.Set):
    """
    Constructed from a list of ranges [a,b)

    invariants:
    __intervals is a list of non-overlapping ranges
    """

    __intervals: list[tuple[int, int]]

    def __init__(self, iterable: Iterable[tuple[int, int] | range] | None = None):
        if iterable is None:
            self.__intervals = []
            return
        self.__intervals = list([((i.start, i.stop) if isinstance(i, range) else i ) for i in iterable])
        self.__normalize()

    def __normalize(self):
        if len(self.__intervals) <= 1:
            return
        self.__intervals.sort(key=lambda x: x[1])
        stack = [self.__intervals[0]]
        for start, stop in self.__intervals[1:]:
            while stack and start < stack[-1][1] and stack[-1][0] < stop:
                final = stack.pop()
                start = min(final[0], start)
                stop = max(final[1], stop)
            stack.append((start, stop))
        self.__intervals = stack

    def __contains__(self, item: int):
        for start, end in self.__intervals:
            if start <= item < end:
                return True
        return False

    def __iter__(self):
        return iter(self.__intervals)

    def __len__(self):
        return len(self.__intervals)
