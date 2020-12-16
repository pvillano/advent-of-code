from itertools import product

data = """..."""

test_data = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

lines = data.rstrip().split("\n")



# or_ones, and_zeros = 0,0
#
# memory = {}
#
# for line in lines:
#     if line.startswith("mask"):
#         mask = line.removeprefix("mask = ")
#         or_ones = int(mask.replace("X", "0"), 2)
#         and_zeros = int(mask.replace("X", "1"), 2)
#     else:
#         line = line.removeprefix("mem[")
#         addr, value = map(int, line.split("] = "))
#         value = (value | or_ones) & and_zeros
#         memory[addr] = value
#
# print(sum(memory.values()))


mask = ""
memory = {}

for line in lines:
    if line.startswith("mask"):
        mask = line.removeprefix("mask = ")
    else:
        line = line.removeprefix("mem[")
        addr, value = map(int, line.split("] = "))
        addr_str = bin(addr).removeprefix('0b').rjust(36, "0")
        sequence = []
        for bit, mask_bit in zip(addr_str, mask):
            if mask_bit == "0":
                sequence.append((bit,))
            elif mask_bit == "1":
                sequence.append(("1",))
            elif mask_bit == "X":
                sequence.append(("0","1"))

        for str_bits in product(*sequence):
            addr_actual = int("".join(str_bits), 2)
            memory[addr_actual] = value

print(sum(memory.values()))



pass