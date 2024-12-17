import sys
from itertools import count

from tqdm import tqdm

from utils import benchmark, get_day, test
from utils.parallel import starmap16
from utils.parsing import extract_ints


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

def part2(raw: str):
    old_registers, program = parse(raw)
    old_registers['A'] = 'a'
    ip = 0
    out = []
    for a in tqdm(count()):
        registers = dict(old_registers)
        if raw == test2:
            if not ((a // (1 << 3)) != 0):
                continue
            if not (((a // (1 << 3)) % 8) == program[0]):
                continue
            if not ((((a // (1 << 3)) // (1 << 3)) % 8) == program[1]):
                continue
            if not (((((a // (1 << 3)) // (1 << 3)) // (1 << 3)) % 8) == program[2]):
                continue
            if not ((((((a // (1 << 3)) // (1 << 3)) // (1 << 3)) // (1 << 3)) % 8) == program[3]):
                continue
            if not (((((((a // (1 << 3)) // (1 << 3)) // (1 << 3)) // (1 << 3)) // (1 << 3)) % 8) == program[4]):
                continue
        else:
            if not ((((((a % 8) ^ 2) ^ (a // (1 << ((a % 8) ^ 2)))) ^ 3) % 8) == program[0]):
                continue
            if not (((((((a // (1 << 3)) % 8) ^ 2) ^ ((a // (1 << 3)) // (1 << (((a // (1 << 3)) % 8) ^ 2)))) ^ 3) % 8) == program[1]):
                continue
            if not ((((((((a // (1 << 3)) // (1 << 3)) % 8) ^ 2) ^ (((a // (1 << 3)) // (1 << 3)) // (1 << ((((a // (1 << 3)) // (1 << 3)) % 8) ^ 2)))) ^ 3) % 8) == program[2]):
                continue
            if not (((((((((a // (1 << 3)) // (1 << 3)) // (1 << 3)) % 8) ^ 2) ^ ((((a // (1 << 3)) // (1 << 3)) // (1 << 3)) // (1 << (((((a // (1 << 3)) // (1 << 3)) // (1 << 3)) % 8) ^ 2)))) ^ 3) % 8) == program[3]):
                continue
            if not True:
                continue
            if not True:
                continue
            if not True:
                continue
            if not True:
                continue
        while ip in range(len(program)):
            op = program[ip]
            literal = program[ip + 1]
            combo = [0, 1, 2, 3, registers['A'], registers['B'], registers['C']][literal]
            match op:
                case 0:
                    registers['A'] = f"({registers['A']} // (1 << {combo}))"
                case 1:
                    registers['B'] = f"({registers['B']} ^ {literal})"
                case 2:
                    registers['B'] = f"({combo} % 8)"
                case 3:
                    if eval(registers['A'], {'a': a}) != 0:
                        ip = literal
                        continue
                    elif len(out) < len(program):
                        # jump skipped when needed
                        print("missed condition:", f"({registers['A']} != 0)")
                        sys.exit(1)
                case 4:
                    registers['B'] = f"({registers['B']} ^ {registers['C']})"
                case 5:
                    out.append(f"({combo} % 8)")
                    if eval(out[-1], {'a': a}) != program[len(out) - 1]:
                        print("missed condition:", f"({out[-1]} == program[{len(out)-1}])")
                        sys.exit(1)
                    if len(out) == len(program):
                        if [eval(expr, {'a': a}) for expr in out] == program:
                            return a

                case 6:
                    registers['B'] = f"({registers['A']} // (1 << {combo}))"
                case 7:
                    registers['C'] = f"({registers['A']} // (1 << {combo}))"
            ip += 2


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
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
