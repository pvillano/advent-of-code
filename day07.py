test_data = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

data = """..."""

# tot = 0
# contains = dict()
#
# lines = data.split("\n")
# for line in lines:
#     part1, part2 = line.split(" contain ")
#     key = part1.replace(" bags", "").replace(" bag", "")
#     if part2.endswith('no other bags.'):
#         contains[key] = []
#     else:
#         part2 = part2[:-1]
#         values = part2.split(", ")
#         contains[key] = [x.split(" ", 1)[1].replace(" bags", "").replace(" bag", "") for x in values]
#
#
# reverse_tree = defaultdict(list)
# for k, v in contains.items():
#     for child in v:
#         reverse_tree[child].append(k)
#
# seen = set()
#
# print(reverse_tree)
#
# def recurse(child):
#     seen.add(child)
#     for desc in reverse_tree[child]:
#         recurse(desc)
# recurse("shiny gold")
#
# print(seen)
# print(len(seen) - 1)


lines = data.split("\n")
contains = dict()
for line in lines:
    part1, part2 = line.split(" contain ")
    key = part1.removesuffix(" bags")
    if part2 == 'no other bags.':
        contains[key] = []
    else:
        part2 = part2.removesuffix(".")
        values = part2.split(", ")
        contains[key] = []
        for value in values:
            count, color_bags = value.split(" ", 1)
            count = int(count)
            color = color_bags.removesuffix(" bag").removesuffix(" bags")
            contains[key].append((color, count))


def recurse(parent):
    tot = 1
    for child_color, child_count in contains[parent]:
        tot += child_count * recurse(child_color)
    return tot


print(recurse("shiny gold") - 1)
