__all__ = ["get_day", "extract_ints"]

import datetime
import os
import re

import requests

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


def extract_ints(line: str) -> tuple[int, ...]:
    str_list = re.findall("(-?[0-9]+)", line)
    return tuple(map(int, str_list))
