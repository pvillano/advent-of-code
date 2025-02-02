__all__ = ["benchmark", "DEBUG", "get_input", "test"]

import datetime
import os
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import requests

from . import printing

has_trace = hasattr(sys, "gettrace") and sys.gettrace() is not None
has_breakpoint = sys.breakpointhook.__module__ != "sys"
DEBUG = has_trace or has_breakpoint

def get_input(__filename__: str) -> str:
    """
    :param __filename__: a path ending in YYYY/dayDD.py
    :return:
    """
    py_path = Path(__filename__)
    year_path, project_root, *_ = py_path.parents
    year = year_path.name
    day = int(py_path.name.removeprefix("day").removesuffix(".py"))
    out_file = project_root.joinpath(".inputs", year, f"input{day:02}.txt")
    token_path = project_root.joinpath(".token")
    # token_path = os.path.join(project_root, ".token")
    if not os.path.exists(out_file):
        Path("").mkdir(parents=True, exist_ok=True)
        with open(token_path, "r") as token_file:
            cookies = {"session": token_file.read()}
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
        response.raise_for_status()
        out_file.parent.mkdir(exist_ok=True, parents=True)
        with open(out_file, "w") as cache_file:
            cache_file.write(response.text)

    with open(out_file) as cache_file:
        return cache_file.read().rstrip("\n")


def test(func: Callable, data, expected):
    name = func.__name__ if hasattr(func, "__name__") else "benchmark"
    out_stream = sys.stderr if DEBUG else sys.stdout
    print("Testing", name, datetime.datetime.now().strftime("%I:%M%p"), file=out_stream, flush=DEBUG)
    start_time = time.perf_counter_ns()
    ans = func(data)
    end_time = time.perf_counter_ns()
    seconds = (end_time - start_time) / 10**9
    if not ans == expected:
        print(f"FAILED in {seconds:0.3f} seconds FAILED FAILED FAILED FAILED ", file=out_stream)
        print("Expected:", expected, file=out_stream)
        print("Actual:  ", ans, file=out_stream)
        print(file=out_stream, flush=DEBUG)
        return False
    else:
        print(f"Passed in {seconds:0.3f} seconds\n", file=out_stream, flush=DEBUG)
        return True


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
    seconds = (end_time - start_time) / 10**9
    printing.pprint(ans, stream=out_stream)
    print(f"Completed in {seconds:0.3f} seconds.\n", file=out_stream, flush=True)
    return ans
