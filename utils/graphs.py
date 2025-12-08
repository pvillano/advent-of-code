__all__ = [
    "AdjacencyListType",
    # "bfs",
    "densify_keys",
    "is_dag",
    "reverse_edges",
    "topological_sort",
]

from collections.abc import Callable, Hashable

type AdjacencyDictType[T: Hashable] = dict[T, list[T]]

type AdjacencyListType = AdjacencyDictType | list[list[int]]


def bfs(graph: AdjacencyListType, key: Callable):
    raise NotImplementedError()


def densify_keys[T: Hashable](adj_list: AdjacencyDictType[T]) -> tuple[list[list[int]], list[T], dict[T, int]]:
    """
    Replaces an adjacency list with arbitrary nodes with one using only ints

    Returns a new adjacency list, a conversion from int to node, and a conversion from node to int
    :param adj_list:
    :return:
    """
    itoa = sorted(adj_list.keys())
    atoi = {val: idx for idx, val in enumerate(itoa)}
    new_adj_list = [[] for _ in range(len(itoa))]
    for key, neighbors in adj_list.items():
        i = atoi[key]
        new_neighbors = list(map(lambda x: atoi[x], neighbors))
        new_adj_list[i] = new_neighbors
    return new_adj_list, itoa, atoi


def is_dag(adj_list: AdjacencyListType) -> bool:
    a = reverse_edges(adj_list)
    b = reverse_edges(a)
    removed_nodes = True
    while removed_nodes:
        removed_nodes = False
        for k, v in tuple(a.items()):
            if len(v) == 0:
                del a[k]
                del b[k]
                removed_nodes = True
            elif k not in b:
                del a[k]
                removed_nodes = True
        for k, v in tuple(b.items()):
            if len(v) == 0:
                del a[k]
                del b[k]
                removed_nodes = True
            elif k not in a:
                del b[k]
                removed_nodes = True
    assert (len(a) == 0) == (len(b) == 0)
    return len(a) == 0


def reverse_edges[T: AdjacencyListType](adj_list: T) -> T:
    """
    Reverses the edges in an adjacency list graph
    """
    new_adj_list = {k: [] for k in adj_list}
    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            new_adj_list[neighbor].append(node)
    return new_adj_list


def topological_sort(adj_list: AdjacencyListType) -> list[int]:
    """

    :param adj_list:
    :return:
    """
    visited = set()
    stack = []

    def _top_sort_helper(v: Hashable):
        visited.add(v)
        for neighbor in adj_list.get(v, []):
            if neighbor not in visited:
                _top_sort_helper(neighbor)
        stack.append(v)

    for key in adj_list:
        if key not in visited:
            _top_sort_helper(key)

    return stack[::-1]


# assert is_dag({0: [1, 2], 1: [2, 3], 2: [3], 3: []})
# assert is_dag({0: [1, 2], 1: [2, 3], 2: [3]})
# assert not is_dag({0: [1, 2], 1: [0]})
