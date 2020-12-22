from collections import deque
from itertools import count

data = """..."""

test_data = """Player 1:
43
19

Player 2:
2
29
14"""


p1, p2 = test_data.split("\n\n")


p1 = deque(map(int, p1.split("\n")[1:]))
p2 = deque(map(int, p2.split("\n")[1:]))


while len(p1) > 0 and len(p2) > 0:
    p1c, p2c = p1.popleft(), p2.popleft()
    if p1c > p2c:
        p1.append(p1c)
        p1.append(p2c)
    elif p2c > p1c:
        p2.append(p2c)
        p2.append(p1c)

print(sum([i * card for i, card in zip(count(1), reversed(p1 + p2))]))

# test data
p1 = deque([9, 2, 6, 3, 1])
p2 = deque([5, 8, 4, 7, 10])

seen = set()


def winner_tuple(p1deck, p2deck, game=1):
    game_round = 1
    while len(p1deck) > 0 and len(p2deck) > 0:
        # print(game, game_round, p1deck, p2deck)
        frozen = (game, tuple(p1deck), tuple(p2deck))
        if frozen in seen:
            return 1
        seen.add(frozen)
        p1c, p2c = p1deck.popleft(), p2deck.popleft()
        if p1c <= len(p1deck) and p2c <= len(p2deck):
            winner = winner_tuple(deque(list(p1deck)[:p1c]), deque(list(p2deck)[:p2c]), game+1)
            if winner == 1:
                p1deck.append(p1c)
                p1deck.append(p2c)
            elif winner == 2:
                p2deck.append(p2c)
                p2deck.append(p1c)
            else:
                print("PAAANIK")
                exit(2)
        elif p1c > p2c:
            p1deck.append(p1c)
            p1deck.append(p2c)
        elif p2c > p1c:
            p2deck.append(p2c)
            p2deck.append(p1c)
        else:
            print("PANIK")
            exit(1)
        game_round += 1
    if game == 1:
        print(sum([i * card for i, card in zip(count(1), reversed(p1deck + p2deck))]))
    if p1deck:
        return 1
    return 2


winner_tuple(p1, p2)