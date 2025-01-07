import re

file = """..."""
# required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
# valid = 0
# for passport in file.split("\n\n"):
#     passport = passport.strip()
#     tokens = passport.split()
#     keys = [token.split(":")[0] for token in tokens]
#     if all([key in keys for key in required]):
#         valid += 1
#
# print(valid)


required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
valid = 0

hclrgx = re.compile("^#[0-9a-fA-F]{6}$")

for passport in file.split("\n\n"):
    passport = passport.strip()
    tokens = passport.split()
    keys = [token.split(":")[0] for token in tokens]
    if not all([key in keys for key in required]):
        continue
    keymap = {token.split(":")[0]: token.split(":")[1] for token in tokens}
    byr = int(keymap["byr"])
    if not 1920 <= byr <= 2002:
        continue
    iyr = int(keymap["iyr"])
    if not 2010 <= iyr <= 2020:
        continue
    eyr = int(keymap["eyr"])
    if not 2020 <= eyr <= 2030:
        continue

    hgt = keymap["hgt"]
    hgt, metric = hgt[:-2], hgt[-2:]
    if hgt == "":
        continue
    else:
        hgt = int(hgt)
    if metric == "cm":
        if not 150 <= hgt <= 193:
            continue
    elif metric == "in":
        if not 59 <= hgt <= 76:
            continue
    else:
        continue

    hcl = keymap["hcl"]
    if not hclrgx.match(hcl):
        continue

    ecl = keymap["ecl"]
    if ecl not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        continue

    pid = keymap["pid"]
    if len(pid) != 9:
        continue
    for i in pid:
        if i not in "0123456789":
            continue

    valid += 1
    print(keymap)

print(valid)
# not 84
