from utils import benchmark, get_day

test = """A Y
B X
C Z"""

lines = get_day(2, test).split("\n")


def part1():
    map_them = {val: idx for idx, val in enumerate("ABC")}
    map_you = {val: idx for idx, val in enumerate("XYZ")}
    score = 0
    for line in lines:
        them, you = line.split(" ")
        score += map_you[you] + 1  # shape points
        if map_them[them] == map_you[you]:  # tie
            score += 3
        elif (map_them[them] + 1) % 3 == map_you[you]:  # win
            score += 6
    return score


def part2():
    map_them = {val: idx for idx, val in enumerate("ABC")}
    # play previous, same, next
    map_move = {"X": -1, "Y": 0, "Z": 1}
    # lose, tie, win
    outcome_points = {"X": 0, "Y": 3, "Z": 6}
    score = 0
    for line in lines:
        them_str, you_str = line.split(" ")
        them_int = map_them[them_str]
        you_int = (map_move[you_str] + them_int) % 3
        score += outcome_points[you_str] + you_int + 1
    return score


if __name__ == "__main__":
    benchmark(part1)
    benchmark(part2)
