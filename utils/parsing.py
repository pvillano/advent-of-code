import os

import requests

from .std import DEBUG

__all__ = ["get_day"]


def get_day(day: int, practice: str = "", *, year: int = 2022, override=False) -> str:
    if DEBUG and not override:
        return practice.rstrip("\n")

    filename = f"input{day:02d}.txt"
    if not os.path.exists(filename):
        with open(".token", "r") as token_file:
            cookies = {"session": token_file.read()}
        response = requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies
        )
        response.raise_for_status()
        with open(filename, "w") as cache_file:
            cache_file.write(response.text)

    with open(filename) as cache_file:
        return cache_file.read().rstrip("\n")
