from typing import Hashable


class UnionFind[T: Hashable]:
    """
    Stores a partition of a set into disjoint subsets
    """

    __toIndex: dict[T, int]
    __toOriginal: list[T]
    __pointers: list[int]
    __ranks: list[int]
    __sizes: list[int]

    def __init__(self, items: list[T]):
        """

        :param items: a list of immutable items to be used as keys
        """
        self.__toOriginal = list(items)
        self.__toIndex = {item: i for i, item in enumerate(items)}
        self.__pointers = list(range(len(items)))
        self.setCount = len(items)
        self.__ranks = [0] * len(items)
        self.__sizes = [1] * len(items)

    def add(self, item: T) -> bool:
        """

        :param item: item to add
        :return: True if item was added, False if it already existed
        """
        if item in self.__toIndex:
            return False
        new_idx = len(self.__toOriginal)
        self.__toOriginal.append(item)
        self.__toIndex[item] = new_idx
        self.__pointers.append(new_idx)
        self.setCount += 1
        self.__ranks.append(0)
        self.__sizes.append(1)
        return True


    def __find(self, x: int) -> int:
        while self.__pointers[x] != x:
            next_x = self.__pointers[x]
            # x is adopted by their grandparent
            grandparent = self.__pointers[self.__pointers[x]]
            self.__pointers[x] = grandparent
            x_old_parent = next_x

            self.__sizes[x_old_parent] -= self.__sizes[x]
            x = next_x
        return x

    def union(self, x_original: T, y_original: T) -> None:
        """
        Puts two elements into the same set.
        """
        x = self.__toIndex[x_original]
        y = self.__toIndex[y_original]
        x = self.__find(x)
        y = self.__find(y)
        # assert x == self.__pointers[x] # invariant from find
        # assert y == self.__pointers[y] # invariant from find
        if x == y:
            return
        # the new parent should have the higher starting rank
        # so that max height does not grow
        if self.__ranks[x] < self.__ranks[y]:
            x, y = y, x
        self.__pointers[y] = x
        self.__sizes[x] += self.__sizes[y]
        self.setCount -= 1
        if self.__ranks[x] == self.__ranks[y]:
            self.__ranks[x] += 1
        return

    def related(self, x_original: T, y_original: T) -> bool:
        """
        returns true if two elements are in the same set
        """
        return self.__find(self.__toIndex[x_original]) == self.__find(self.__toIndex[y_original])


    def __iter__(self):
        pass
