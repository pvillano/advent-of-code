# REMEMBER TO PASTE IN THE DATA

test_data = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

data = """..."""

lines = data.rstrip().split("\n")
lines = [int(x) for x in lines]

twofive = 25

ideal = 248131121

# def isok(i):
#     for j in range(twofive):
#         for k in range(twofive):
#             if lines[i - j - 1] + lines[i - k - 1] == lines[i]:
#                 return True
#     return False
#
#
# try:
#     for i in range(twofive, len(lines)):
#         if not isok(i):
#             print(lines[i])
# except IndexError:
#     exit(1)

for i in range(len(lines)):
    for j in range(i, len(lines)):
        region = lines[i:j]
        if sum(region) == ideal:
            print(i, j, max(region) + min(region))
