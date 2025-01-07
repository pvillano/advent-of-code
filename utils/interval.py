import collections
from collections.abc import Iterable


def range_overlaps(a: range, b: range):
    return a.start < b.stop and b.start < a.stop


class IntervalSet(collections.abc.Set):
    """
    Can be constructed from
    a list of ranges [a,b)

    invariants:
    __intervals is a list of non-overlapping ranges
    """

    __intervals: list[tuple[int, int]]

    def __init__(self, __iterable: Iterable[tuple[int, int]] = None):
        if __iterable is None:
            self.__intervals = []
            return
        self.__intervals = list(__iterable)
        self.__normalize()

    def __normalize(self):
        if len(self.__intervals) == 0:
            return
        self.__intervals.sort()
        new = [self.__intervals[0]]
        for r in self.__intervals[1:]:
            start, end = new[-1]
            if start <= r[0] < end:
                stop = max(new[-1][1], r[1])
                new[-1] = (new[-1][0], stop)
        self.__intervals = new

    def __contains__(self, item: int):
        for start, end in self.__intervals:
            if start <= item < end:
                return True
        return False

    def __iter__(self):
        return iter(self.__intervals)

    def __len__(self):
        return len(self.__intervals)
