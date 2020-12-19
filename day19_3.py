import time

from otqdm import otqdm
from utils import debug_print, flatten

data = """..."""

test_data = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""





rules_lines, data_lines = data.split("\n\n")
data_lines = data_lines.split("\n")
rules = dict()

for line in rules_lines.split("\n"):
    val:str
    key, val = line.split(":")
    key = int(key)
    val = val.strip()
    if "a" in val:
        rules[key] = "a"
    elif "b" in val:
        rules[key] = "b"
    else:
        options = val.split(" | ")
        things = []
        for option in options:
            nums = map(int, option.split(" "))
            things.append(tuple(nums))
        rules[key] = tuple(things)


rules[8] = ((42,),(42,8))
rules[11] = (42,31),(42,11,31)

max_rule_w = max(len(str(x)) for x in rules.keys())

def poss_rem_after_applying(s: str, rule:int, rec_level = 0):
    """yields possible remainder strings"""
    print(" ." * rec_level, str(rule).rjust(max_rule_w), s)
    if s == "FUCK":
        yield "FUCK"
        return

    val = rules[rule]
    if val == "a" or val == "b":
        if s == val:
            yield "FUCK YES"
            return
        elif s[0] == val:
            yield str(s[1:])
            return
        else:
            yield "FUCK"
            return

    womp = []
    for r in val:
        somp = [s]
        for i in r:
            somp = list(flatten(poss_rem_after_applying(x, i, rec_level+1) for x in somp))
        womp.append(somp)
    yield from list(flatten(womp))

tot = 0
for line in otqdm(data_lines[0:1]):
    for blah in poss_rem_after_applying(line, 0):
        if blah == "FUCK YES":
            tot += 1
            break
print(tot)





start_time = time.time()