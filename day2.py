# goodwords = 0
# for line in open("day02.txt"):
#     stripped = line.strip()
#     counts, char, pwd = stripped.split()
#     min_count, max_count = counts.split("-")
#     min_count, max_count = int(min_count), int(max_count)
#     char = char[0]
#     actual_count = 0
#     for ch in pwd:
#         if ch == char:
#             actual_count+=1
#     if min_count <= actual_count <= max_count:
#         print(line)
#         goodwords +=1
#
# print(goodwords)

goodwords = 0
for line in open("day02.txt"):
    stripped = line.strip()
    counts, char, pwd = stripped.split()
    min_count, max_count = counts.split("-")
    min_count, max_count = int(min_count), int(max_count)
    char = char[0]
    try:
        if (pwd[min_count - 1] == char) + (pwd[max_count - 1] == char) == 1:
            goodwords += 1
    except IndexError:
        pass

print(goodwords)

# 182 too low
