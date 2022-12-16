from math import log, exp
from time import time, sleep
from typing import Sized, Iterable

__all__ = ["otqdm"]

UTF = " " + "".join(map(chr, range(0x258F, 0x2587, -1)))


def format_interval(t):
    """[H:]MM:SS"""
    if t is None:
        return "??:??"
    mins, s = divmod(int(t), 60)
    h, m = divmod(mins, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    else:
        return f"{m:02d}:{s:02d}"


def otqdm(
    iterator: Sized and Iterable,
    min_interval=1,
    min_iters=1,
    unit="it/s",
    n_bars=10,
    percent_is_time=False,
    bars_is_time=False,
    len_iterator=None,
):

    last_print_t = start_time = time()
    last_print_n = 0
    n = 0
    last_len = 0
    remaining = None
    n_syms = len(UTF) - 1
    if len_iterator is None:
        try:
            len_iterator = len(iterator)
        except TypeError:
            pass

    for obj in iterator:
        yield obj
        n += 1
        if n - last_print_n >= min_iters or n == len_iterator:
            delta_t = time() - last_print_t
            if delta_t >= min_interval or n == len_iterator:
                now = time()
                elapsed = now - start_time
                elapsed_str = format_interval(elapsed)
                rate = n / elapsed if elapsed > 0 else 0

                elapsed_prev = last_print_t - start_time

                if last_print_n and elapsed_prev:
                    exponent = log(elapsed / elapsed_prev) / log(n / last_print_n)
                    if 0.05 <= exponent < 9.95:
                        k = elapsed / (n**exponent)
                        big_o_str = f"O(n^{exponent:3.1f})"
                        if len_iterator is not None:
                            remaining = k * (len_iterator**exponent) - elapsed
                    else:
                        base = exp(log(elapsed / elapsed_prev) / (n - last_print_n))
                        if 0.05 <= base < 9.95:
                            k = elapsed / (base**n)
                            big_o_str = f"O({base:3.1f}^n)"
                            if len_iterator is not None:
                                remaining = k * (base**len_iterator) - elapsed
                        else:
                            big_o_str = "O(?????)"
                            remaining = None
                else:
                    big_o_str = "O(?????)"
                    remaining = None

                remaining_str = format_interval(remaining)

                if len_iterator is not None:
                    time_percent = elapsed / (remaining + elapsed) if remaining is not None else 0
                    count_percent = n / len_iterator
                    percent = time_percent if percent_is_time else count_percent
                    percent_b = time_percent if bars_is_time else count_percent

                    bar_length, frac_bar_length = divmod(
                        int(percent_b * n_bars * n_syms), n_syms
                    )
                    bar_str = UTF[-1] * bar_length
                    if bar_length < n_bars:  # whitespace padding
                        bar_str = (
                            bar_str
                            + UTF[frac_bar_length]
                            + UTF[0] * (n_bars - bar_length - 1)
                        )

                    s = f"{big_o_str} {percent * 100:3.0f}%|{bar_str}| {n}/{len_iterator} [{elapsed_str}/{remaining_str}, {rate:5.2f}{unit}]"

                else:
                    s = f"{big_o_str} ??%|??????????| {n}/{'?'*len(str(n))} [{elapsed_str}/{remaining_str}, {rate:5.2f}{unit}]"

                len_s = len(s)
                print('\r' + s + (' ' * max(last_len - len_s, 0)), end="")
                last_len = len_s

                last_print_n = n
                last_print_t = now
    print()


if __name__ == "__main__":

    def fibonacci(i):
        if i < 2:
            return 1
        return fibonacci(i - 1) + fibonacci(i - 2)

    print(">>>for i in otdqm(range(40)):\n" "...    sleep(i/100)")
    for i in otqdm(range(40)):
        sleep(i / 100)

    print(">>>for i in otdqm(range(40)):\n" "...    fibonacci(i)")
    for i in otqdm(range(40)):
        fibonacci(i)
