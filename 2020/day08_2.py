from copy import copy

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


# for excluded in range(len(lines)):
#     if lines[excluded].split(" ")[0] != "jmp":
#         continue
#
#     accumulator = 0
#     instruction_ptr = 0
#     executed_instructions = set()
#
#     try:
#         while instruction_ptr not in executed_instructions:
#             executed_instructions.add(instruction_ptr)
#             code, value = get_line(instruction_ptr).split(" ")
#             value = int(value)
#             if code == "acc":
#                 accumulator += value
#                 instruction_ptr += 1
#             elif code == "jmp":
#                 instruction_ptr += value
#             elif code == "nop":
#                 instruction_ptr += 1
#     except IndexError:
#         print(instruction_ptr, accumulator)
#         exit(0)


class Interpreter:
    def __init__(self, lines):
        self.accumulator = 0
        self.instruction_ptr = 0
        self.executed_instructions = set()
        self.lines = copy(lines)

    def run(self):
        try:
            while self.instruction_ptr not in self.executed_instructions:
                code, *values = self.lines[self.instruction_ptr].split(" ")
                values = [int(value) for value in values]
                getattr(self, code)(*values)
                self.executed_instructions.add(self.instruction_ptr)
        except IndexError:
            return self.accumulator
        return None

    def acc(self, value):
        self.accumulator += value
        self.instruction_ptr += 1

    def jmp(self, value):
        self.instruction_ptr += value

    def nop(self, _):
        self.instruction_ptr += 1

    def example(self, value1, value2):
        something = value1 * value2


for i in range(len(lines)):
    if lines[i].startswith("nop"):
        my_lines = copy(lines)
        my_lines[i] = "jmp" + lines[i][3:]
        result = Interpreter(my_lines).run()
        if result is not None:
            print(result)
            exit(0)
    if lines[i].startswith("jmp"):
        my_lines = copy(lines)
        my_lines[i] = "nop" + lines[i][3:]
        result = Interpreter(my_lines).run()
        if result is not None:
            print(result)
            exit(0)
