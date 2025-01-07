from collections import Counter

test_data = """16
10
15
5
1
11
7
19
6
12
4"""

data = """..."""

lines = data.rstrip().split("\n")

nums = [int(x) for x in lines]
nums.sort()
nums = [0] + nums + [nums[-1] + 3]
pairs = zip(nums[:-1], nums[1:])
diffs = [b - a for a, b in pairs]
diff_counts = Counter(diffs)
print(diff_counts[1] * diff_counts[3])

# combos_ending_w_i
combos = [0] * len(nums)
combos[0] = 1
for i in range(1, len(nums)):
    cur = 0
    if i >= 1 and nums[i] - nums[i - 1] <= 3:
        cur += combos[i - 1]
    if i >= 2 and nums[i] - nums[i - 2] <= 3:
        cur += combos[i - 2]
    if i >= 3 and nums[i] - nums[i - 3] <= 3:
        cur += combos[i - 3]
    combos[i] = cur

print(combos[-1])
