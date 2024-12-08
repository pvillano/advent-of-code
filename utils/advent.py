__all__ = [
    "benchmark",
    "DEBUG",
    "get_day",
    "test"
]

import datetime
import os
import sys
import time
from collections.abc import Callable
from typing import Any

import requests

from . import printing

has_trace = hasattr(sys, 'gettrace') and sys.gettrace() is not None
has_breakpoint = sys.breakpointhook.__module__ != "sys"
DEBUG = has_trace or has_breakpoint

THIS_YEAR = datetime.datetime.today().year


def get_day(day: int) -> str:
    """
    :param day:
    :return:
    """

    filename = f"input{day:02d}.txt"
    if not os.path.exists(filename):
        with open(".token", "r") as token_file:
            cookies = {"session": token_file.read()}
        response = requests.get(
            f"https://adventofcode.com/{THIS_YEAR}/day/{day}/input", cookies=cookies
        )
        response.raise_for_status()
        with open(filename, "w") as cache_file:
            cache_file.write(response.text)

    with open(filename) as cache_file:
        return cache_file.read().rstrip("\n")


def test(func: Callable, data, expected):
    name = func.__name__ if hasattr(func, "__name__") else "benchmark"
    out_stream = sys.stderr if DEBUG else sys.stdout
    print("Testing", name, datetime.datetime.now().strftime("%I:%M%p"), file=out_stream, flush=DEBUG)
    start_time = time.perf_counter_ns()
    ans = func(data)
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10 ** 9
    if not ans == expected:
        print(f"FAILED in {seconds:0.3f} seconds FAILED FAILED FAILED FAILED FAILED FAILED FAILED FAILED FAILED", file=out_stream)
        print("Expected:", expected, file=out_stream)
        print("Actual:  ", ans, file=out_stream)
        print(file=out_stream, flush=DEBUG)
    else:
        print(f"Passed in {seconds:0.3f} seconds\n", file=out_stream, flush=DEBUG)


def benchmark(func: Callable, *args, **kwargs) -> Any:
    """
    Calls a function and prints the return value
    :param func:
    :return: None
    """
    out_stream = sys.stderr if DEBUG else sys.stdout
    name = func.__name__ if hasattr(func, "__name__") else "benchmark"
    print("Started", name, datetime.datetime.now().strftime("%I:%M%p"), file=out_stream, flush=True)
    start_time = time.perf_counter_ns()
    ans = func(*args, **kwargs)
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10 ** 9
    printing.pprint(ans, stream=out_stream)
    print(f"Completed in {seconds:0.3f} seconds.\n", file=out_stream, flush=True)
    return ans
