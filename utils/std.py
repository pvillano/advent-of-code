__all__ = [
    "benchmark",
    "DEBUG",
    "flatten",
    "pipe"
]

import os
import sys
import time
import datetime
from itertools import chain
from pprint import pprint as not_my_pp
from typing import Callable

import requests as requests

DEBUG = bool(sys.gettrace())

flatten = chain.from_iterable


def pipe(first, *args: Callable):
    for func in args:
        first = func(first)
    return first


def pprint(object_, stream=None, indent=1, width=80, depth=None, *,
           compact=False, sort_dicts=True, underscore_numbers=False):
    if isinstance(object_, str):
        print('"""', file=stream)
        print(object_.replace("\\", "\\\\"))
        print('"""', file=stream)
    else:
        not_my_pp(object_, stream, indent, width, depth, compact=compact, sort_dicts=sort_dicts,
                  underscore_numbers=underscore_numbers)


def test(part: Callable, data, expected=None):
    start_time = time.perf_counter_ns()
    ans = part(data)
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10 ** 9
    if DEBUG:
        pprint(ans, stream=sys.stderr)
        print(
            f"completed in {seconds:0.3f} seconds\n", file=sys.stderr, flush=True
        )
    else:
        pprint(ans)
        print(f"completed in {seconds:0.3f} seconds\n")
    assert ans == expected


def benchmark(func: Callable, *args, **kwargs) -> None:
    """
    Calls a function and prints the return value
    :param func:
    :return: None
    """
    out_stream = sys.stderr if DEBUG else sys.stdout
    print("Started", datetime.datetime.now().strftime("%I:%M%p"), file=out_stream, flush=True)
    start_time = time.perf_counter_ns()
    ans = func(*args, **kwargs)
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10 ** 9
    pprint(ans, stream=out_stream)
    print(f"Completed in {seconds:0.3f} seconds.\n", file=out_stream, flush=True)
    return ans
