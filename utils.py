import sys

__all__ = [
    "DEBUG",
    "flatten",
    "debug_print",
    "getlines"
]

from itertools import chain

gettrace = getattr(sys, 'gettrace', bool)

DEBUG = bool(gettrace())

flatten = chain.from_iterable


def debug_print(*args, **kwargs):
    if DEBUG:
        return print(*args, **kwargs)


def getlines(data:str, test_data:str, sep:str="\n"):
    if DEBUG:
        return test_data.rstrip().split(sep)
    else:
        return data.rstrip().split(sep)
