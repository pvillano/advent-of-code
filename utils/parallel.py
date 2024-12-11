import multiprocessing
from collections.abc import Callable, Iterable, Collection
from itertools import chain, batched, starmap

import trio
import trio_parallel


async def __parallel_starmap[T](function: Callable[[...], T], collection: Collection[Iterable]) -> list[T]:
    results = [None] * len(collection)

    async def worker(j, inp):
        results[j] = await trio_parallel.run_sync(function, *inp)

    async with trio.open_nursery() as nursery:
        for i, inp in enumerate(collection):
            nursery.start_soon(worker, i, inp)

    return results


def parallel_starmap[T](function: Callable[[...], T], collection: Collection[Iterable]) -> list[T]:
    return trio.run(__parallel_starmap, function, collection)


def xstarmap[T](function: Callable[[...], T], iterable: Iterable[Iterable]) -> list[T]:
    return list(starmap(function, iterable))


def clamp[T](x: T, min_val: T, max_val: T) -> T:
    return min(max(x, min_val), max_val)


async def __starmap16[T](function: Callable[[...], T], collection: Collection[Iterable]) -> list[T]:
    batches = list(batched(collection, (len(collection) + 15) // 16))
    assert clamp(len(collection), 0, 8) < len(batches) <= 16, f"{len(collection)=} {len(batches)=} {16=}"
    result_batches = [[] for _ in batches]

    async def worker(i, batch):
        result_batches[i] = await trio_parallel.run_sync(xstarmap, function, batch)

    async with trio.open_nursery() as nursery:
        for i, batch in enumerate(batches):
            nursery.start_soon(worker, i, batch)

    return list(chain.from_iterable(result_batches))


def starmap16[T](function: Callable[[...], T], collection: Collection[Iterable]) -> list[T]:
    return trio.run(__starmap16, function, collection)


def double(x):
    return 2 * x


if __name__ == "__main__":
    multiprocessing.freeze_support()