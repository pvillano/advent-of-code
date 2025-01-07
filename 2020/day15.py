from otqdm import otqdm

test_data = """0,3,6"""

data = """18,11,9,0,5,1"""

my_data = list(map(int, data.split(",")))
# my_data.reverse()

# seen: list[int] = my_data
# for i in tqdm(range(30000000 - len(my_data))):
#     try:
#         idx = seen[1:].index(seen[0])
#         seen.insert(0, idx + 1)
#     except ValueError:
#         seen.insert(0, 0)
#
#
# print(seen)

data = list(map(int, data.split(",")))
last_seen = {num: idx for idx, num in enumerate(data[:-1])}
prev = my_data[-1]
for i in otqdm(range(len(my_data), 30000000)):
    if prev not in last_seen:
        last_seen[prev] = i - 1
        prev = 0
    else:
        lsp = last_seen[prev]
        last_seen[prev] = i - 1
        prev = i - lsp - 1

print(prev)