from typing import List

data = """..."""

test_data = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""


rules_lines, data_lines = test_data.split("\n\n")
data_lines = data_lines.split("\n")

rules = dict()

for line in rules_lines.split("\n"):
    rule_id, sub_rule_str = line.split(": ")
    rule_id = int(rule_id)
    if "a" in sub_rule_str:
        rules[rule_id] = "a"
    elif "b" in sub_rule_str:
        rules[rule_id] = "b"
    else:
        sub_rules = []
        for sub_rule in sub_rule_str.split(" | "):
            sub_rules.append(tuple(map(int, sub_rule.split(" "))))  # map is lazy
        rules[rule_id] = sub_rules


rules[8] = [(42,), (42, 8)]
rules[11] = [(42, 31), (42, 11, 31)]


def remainders(msgs: List[str], rule_id: int, rec_depth: int = 0) -> List[str]:
    print(". " * rec_depth, rule_id, msgs)
    if len(msgs) == 0:
        return []  # early out
    rule_list_set = rules[rule_id]
    if rule_list_set in ("a", "b"):  # remove first char, ignore empty/unmatching msgs
        return [msg[1:] for msg in msgs if msg != "" and msg[0] == rule_list_set]

    all_trimmed_msgs = []
    for rule_list in rule_list_set:  # e.g. [(42,), (42, 8)]
        new_msgs = msgs
        for next_rule in rule_list:  # e.g. (42, 8)
            new_msgs = remainders(new_msgs, next_rule, rec_depth + 1)
        all_trimmed_msgs.extend(new_msgs)
    return all_trimmed_msgs


print(sum("" in remainders([msg], 0) for msg in data_lines))
