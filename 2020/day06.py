test_data = """abc

a
b
c

ab
ac

a
a
a
a

b"""

data = """..."""

groups = data.split("\n\n")
tot = 0
for group in groups:
    common_set = set(group.replace("\n", ""))
    for line in group.split("\n"):
        common_set = common_set.intersection(line)
    tot += len(common_set)
print(tot)
