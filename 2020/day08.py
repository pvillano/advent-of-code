test_data = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

data = """..."""

lines = data.rstrip().split("\n")
lines = [x.rstrip() for x in lines]

excluded = 0


def get_line(idx):
    if idx == excluded:
        return "nop +0"
    else:
        return lines[idx]


for excluded in range(len(lines)):
    if lines[excluded].split(" ")[0] != "jmp":
        continue

    accumulator = 0
    instruction_ptr = 0
    executed_instructions = set()

    try:
        while instruction_ptr not in executed_instructions:
            executed_instructions.add(instruction_ptr)
            code, value = get_line(instruction_ptr).split(" ")
            value = int(value)
            if code == "acc":
                accumulator += value
                instruction_ptr += 1
            elif code == "jmp":
                instruction_ptr += value
            elif code == "nop":
                instruction_ptr += 1
    except IndexError:
        print(instruction_ptr, accumulator)
        exit(0)
