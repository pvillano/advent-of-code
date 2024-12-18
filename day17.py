import sys
from dataclasses import dataclass
from itertools import count

from tqdm import tqdm

from utils import benchmark, get_day, test
from utils.parallel import starmap16
from utils.parsing import extract_ints
from utils.printing import debug_print


def parse(raw: str):
    registers, program = raw.split("\n\n")
    registers = registers.splitlines()
    registers = {lhs[-1]: int(rhs) for lhs, rhs in [r.split(": ") for r in registers]}
    program = list(extract_ints(program))
    return registers, program


def part1(raw: str):
    registers, program = parse(raw)
    ip = 0
    out = []
    while ip in range(len(program)):
        op = program[ip]
        literal = program[ip + 1]
        combo = [0, 1, 2, 3, registers['A'], registers['B'], registers['C']][literal]

        match op:
            case 0:
                num = registers['A']
                denom = 1 << combo
                registers['A'] = num // denom
            case 1:
                registers['B'] ^= literal
            case 2:
                registers['B'] = combo % 8
            case 3:
                if registers['A'] != 0:
                    ip = literal
                    continue
            case 4:
                registers['B'] ^= registers['C']
            case 5:
                out.append(combo%8)
            case 6:
                num = registers['A']
                denom = 1 << combo
                registers['B'] = num // denom
            case 7:
                num = registers['A']
                denom = 1 << combo
                registers['C'] = num // denom
        ip += 2
    return ','.join(map(str, out))

def work(registers, program, a_iter):
    old_registers = registers
    for a in a_iter:
        registers = dict(old_registers)

        ip = 0
        out = []
        while ip in range(len(program)):
            op = program[ip]
            literal = program[ip + 1]
            combo = [0, 1, 2, 3, registers['A'], registers['B'], registers['C']][literal]
            match op:
                case 0:
                    num = registers['A']
                    denom = 1 << combo
                    registers['A'] = num // denom
                case 1:
                    registers['B'] ^= literal
                case 2:
                    registers['B'] = combo % 8
                case 3:
                    if registers['A'] != 0:
                        ip = literal
                        continue
                case 4:
                    registers['B'] ^= registers['C']
                case 5:
                    out.append(combo%8)
                case 6:
                    num = registers['A']
                    denom = 1 << combo
                    registers['B'] = num // denom
                case 7:
                    num = registers['A']
                    denom = 1 << combo
                    registers['C'] = num // denom
            ip += 2
        if out == program:
            return a


# def part2(raw: str):
#     registers, program = parse(raw)
#     return starmap16(work, [[registers, program, count(offset, 16)] for offset in range(16)])

@dataclass
class Shifted:
    value: str
    offset: int
    def __str__(self):
        return f"{self.value}[{self.offset}:]"

def part22(raw: str):
    old_registers, program = parse(raw)
    jump_conditions = []
    out_conditions = []
    ip = 0
    registers = dict(old_registers)
    registers['A'] = Shifted('a', 0)
    while ip in range(len(program)):
        op = program[ip]
        literal = program[ip + 1]
        combo = [0, 1, 2, 3, registers['A'], registers['B'], registers['C']][literal]
        match op:
            case 0:
                assert combo == 3
                if isinstance(registers['A'], Shifted):
                    registers['A'] = Shifted(registers['A'].value, registers['A'].offset + 1)
                else:
                    registers['A'] = f"({registers['A']} << {combo})"
            case 1:
                registers['B'] = f"({registers['B']} ^ {literal})"
            case 2:
                if isinstance(combo, Shifted):
                    registers['B'] = f"{combo.value}[{combo.offset}]"
                else:
                    registers['B'] = f"{combo}[0]"
            case 3:
                if len(out_conditions) < len(program):
                    jump_conditions.append(f"{registers['A']} != 0")
                ip = literal
                continue
            case 4:
                registers['B'] = f"({registers['B']} ^ {registers['C']})"
            case 5:
                out_conditions.append(f"{combo}[0] == {program[len(out_conditions) - 1]}")
                assert literal in range(4, 8)
                registers['0123ABC'[literal]] = str(program[len(out_conditions) - 1])
                if len(out_conditions) == len(program):
                    break
            case 6:
                registers['B'] = f"({registers['A']} >> {combo})"
            case 7:
                registers['C'] = f"({registers['A']} >> {combo})"
        ip += 2
    for i in jump_conditions:
        print(i)
    for i in reversed(out_conditions):
        print(i)

def part2(raw):
    part22(raw)
    registers, program = parse(raw)
    candidates = list(range(2**9))
    for i in reversed(range(16)):
        new_candidates = []
        for a0 in candidates:
            for da in range(8):
                a = a0 + da
                if (((a % 8) ^ 2 ^ (a >> (a % 8))) ^ 3) % 8 == program[i]:
                    new_candidates.append(a * 8)
        if i == 1:
            pass
        candidates = new_candidates
    a = min(candidates)
    assert a < 4865100593967448
    assert a < 432075869381536
    return a

test1 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

expected1 = "4,6,3,5,6,3,5,2,1,0"

test2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
expected2 = 117440


def main():
    test(part1, test1, expected1)
    raw = get_day(17)
    benchmark(part1, raw)
    # not 1,5,4,3,5,0,0,4,0
    #     1,7,2,1,4,1,5,4,0
    # test(part2, test2, expected2)
    benchmark(part2, raw)



if __name__ == "__main__":
    main()