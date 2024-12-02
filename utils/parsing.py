__all__ = ["extract_ints"]

import re


def extract_ints(line: str) -> tuple[int, ...]:
    str_list = re.findall("(-?[0-9]+)", line)
    return tuple(map(int, str_list))
